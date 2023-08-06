import json
import logging
import os
import time
from datetime import (
    datetime,
    timedelta,
)
from distutils.util import (
    strtobool,
)
from functools import (
    cached_property,
)
from select import (
    select,
)

import psycopg2
from psycopg2 import (
    sql,
)
from psycopg2.extras import (
    LogicalReplicationConnection,
    wait_select,
)

from replisync.consts import (
    ACTIONS,
    WAL2JSON_CONFIGURATION_PARAMETERS,
    WRITE_IN_CHUNKS,
)
from replisync.errors import (
    ConfigError,
)
from replisync.helpers import (
    int_to_lsn,
)


logger = logging.getLogger('replisync')


class BaseReceiver(object):

    def __init__(
        self,
        slot=None,
        dsn=None,
        message_cb=None,
        block=True,
        plugin='replisome',
        options=None,
        flush_interval=10,
        block_wait=2.0,
    ):
        self.slot = slot
        self.dsn = dsn
        self.plugin = plugin
        self.options = options or []
        if message_cb:
            self.message_cb = message_cb
        self.connection = None
        self.cursor = None
        self.is_running = False
        self.is_blocking = block
        self._shutdown_pipe = os.pipe()
        self.next_wait_time = None
        self.blocking_wait = block_wait

        self.flush_delta = None
        # LSN указанный в data_start последнего сообщения
        self.flush_lsn = 0
        # Наибольший зафиксированный LSN в сообщении
        self.max_flush_lsn = 0
        # Последний зафиксированный LSN в методе send_feedback
        self.last_sent_flush_lsn = 0
        if flush_interval > 0:
            self.flush_delta = timedelta(seconds=flush_interval)

        logger.info(f'Receiver initialized with options: {options}')

    @cached_property
    def write_in_chunks(self):
        """
        Возвращает значение свойства write-in-chunks
        """
        write_in_chunks_options = list(filter(lambda option: option[0] == WRITE_IN_CHUNKS, self.options))

        return strtobool(write_in_chunks_options[0][1]) if write_in_chunks_options else False

    def verify(self):
        """
        Verifies that the receiver is correctly configured and raises error if
        any issues found. May check server for installed plugins, etc.

        :raises ReplisyncError: if verification fails
        """
        pass

    @classmethod
    def from_config(cls, config):
        return cls(options={})

    def __del__(self):
        self.stop()

    def stop(self):
        os.write(self._shutdown_pipe[1], b'stop')

    def close(self):
        logger.info(f'Closing DB connection for {self.__class__.__name__}')

        if self.cursor:
            try:
                # do final flush of last successful message on shutdown
                if self.flush_lsn > 0:
                    self.cursor.send_feedback(flush_lsn=self.flush_lsn)
                    wait_select(self.connection)
                self.cursor.close()
            except Exception:
                logger.exception('Failed to close connection cursor')

            self.cursor = None

        if self.connection:
            try:
                self.connection.close()
            except Exception:
                logger.exception('Failed to close connection')

            self.connection = None

    def update_status_time(self):
        if self.flush_delta is not None:
            self.next_wait_time = datetime.utcnow() + self.flush_delta

    def start(self, lsn=None, **kwargs):
        if not self.slot:
            raise AttributeError('no slot specified')

        if 'block' in kwargs:
            self.is_blocking = kwargs['block']

        self.create_slot()

        if lsn is None:
            lsn = self.get_restart_lsn()

        self.create_connection()

        logger.info(f'starting streaming from slot "{self.slot}" at LSN {lsn}')

        stmt = self._get_replication_statement(self.connection, lsn)
        self.cursor.start_replication_expert(stmt, decode=False)
        wait_select(self.connection)

        self.flush_lsn = 0
        self.update_status_time()

        if self.is_blocking:
            logger.debug(f'Listening to replication slot {self.slot}')
            self.is_running = True
            try:
                while self.is_running:
                    self.on_loop(wait_time=self.blocking_wait)
            except Exception:
                self.close()
                raise
            except KeyboardInterrupt:
                self.destroy()
                raise

    def send_feedback(self):
        """
        Фиксация максимального LSN, как прочитанного из слота, если LSN не был отправлен ранее
        """
        if (
            self.flush_delta is None
            or self.next_wait_time < datetime.utcnow()
        ) and self.max_flush_lsn != self.last_sent_flush_lsn:
            self.cursor.send_feedback(flush_lsn=self.max_flush_lsn)
            self.last_sent_flush_lsn = self.max_flush_lsn

            logger.info(
                f'sending at lsn {int_to_lsn(self.max_flush_lsn)} (int: {self.max_flush_lsn}), '
                f'timestamp - {self.cursor.feedback_timestamp}')

            self.update_status_time()

    def on_loop(self, wait_time=2.0):
        start = datetime.utcnow()
        msg = self.cursor.read_message()
        log_loop = False

        if msg:
            log_loop = True

            self.consume(msg)

            self.flush_lsn = msg.data_start

            # Обновление значения максимального LSN, если пришло большее значение. Может быть, что приходит меньшее
            # значение, не ясно, почему так. Если посмотреть изменения при помощи запроса
            # SELECT * FROM pg_logical_slot_peek_changes('<slot_name>', NULL, NULL);
            # то будет обнаружен отличный LSN (новый максимальный), от пришедшего с сервера в параметре data_start
            self.max_flush_lsn = self.flush_lsn if self.flush_lsn > self.max_flush_lsn else self.max_flush_lsn

            # Попытка отправки lsn
            self.send_feedback()

            logger.debug(
                f'flush_lsn {int_to_lsn(self.flush_lsn)}, {self.flush_lsn}\n'
                f'max_flush_lsn {int_to_lsn(self.max_flush_lsn)}, {self.max_flush_lsn}\n'
                f'last_sent_flush_lsn {int_to_lsn(self.last_sent_flush_lsn)}, {self.last_sent_flush_lsn}\n'
                f'msg.data_start {int_to_lsn(msg.data_start)}, {msg.data_start}\n'
                f'msg.wal_end {int_to_lsn(msg.wal_end)}, {msg.wal_end}'
            )
        else:
            # wait for shutdown or DB connection data, if any forthcoming
            result = select([self._shutdown_pipe[0], self.connection], [], [], wait_time)

            # shutdown requested, clean up
            if self._shutdown_pipe[0] in result[0]:
                self.is_running = False
                self.close()
            else:
                # Попытка отправки lsn
                self.send_feedback()

        if log_loop:
            end = datetime.utcnow()

            logger.debug(f'loop code ended, total seconds: {(end - start).total_seconds()}\n\n')

    def _get_replication_statement(self, cnn, lsn) -> str:
        bits = [
            sql.SQL('START_REPLICATION SLOT '),
            sql.Identifier(self.slot),
            sql.SQL(' LOGICAL '),
            sql.SQL(lsn)]

        if self.options:
            bits.append(sql.SQL(' ('))
            for k, v in self.options:
                bits.append(sql.Identifier(k))
                if v is not None:
                    bits.append(sql.SQL(' '))
                    bits.append(sql.Literal(v))
                bits.append(sql.SQL(', '))
            bits[-1] = sql.SQL(')')

        rv = sql.Composed(bits).as_string(cnn)

        logger.debug(f'replication statement: {rv}')

        return rv

    def process_payload(self, raw_payload):
        """
        Converts the raw payload bytes from the most recent replication chunk
        and invokes the message callback if appropriate

        :param raw_payload: bytes object containing most recent chunk payload
        """
        raise NotImplementedError(f'Missing `process_payload` definition for receiver {self.__class__.__name__}')

    def _log_connection_notices(self):
        """
        Вывод в лог нотификации соединения
        """
        if self.connection.notices:
            for n in self.connection.notices:
                logger.debug(f'server: {n.rstrip()}')

            del self.connection.notices[:]

    def consume(self, raw_chunk):
        """
        Обработка сообщения
        """
        self._log_connection_notices()

        self.process_payload(raw_chunk.payload)

    def message_cb(self, obj):
        logger.info(f'message received: {obj}')

    def create_connection(self):
        logger.info(f'connecting to source database at "{self.dsn}"')

        cnn = psycopg2.connect(
            self.dsn,
            async_=True,
            connection_factory=LogicalReplicationConnection,
        )

        wait_select(cnn)

        self.connection = cnn
        self.cursor = cnn.cursor()

    def get_restart_lsn(self):
        """
        Returns the restart LSN for the replication slot as stored in the
        pg_replication_slots DB table. Returns default start position if
        slot doesn't exist.

        :return: string containing restart LSN for current slot
        """
        command = """
        SELECT restart_lsn FROM pg_replication_slots WHERE slot_name = %s;
        """

        lsn = '0/0'

        try:
            with psycopg2.connect(self.dsn) as conn, conn.cursor() as cursor:
                cursor.execute(command, [self.slot])
                result = cursor.fetchone()
                if result:
                    lsn = result[0]
        except psycopg2.Error as e:
            logger.error(f'error retrieving LSN: {e}')

        return lsn

    def create_slot(self):
        """
        Creates the replication slot, if it hasn't been created already.
        """
        logger.info(f'creating replication slot "{self.slot}" with plugin {self.plugin}')

        command = """
            WITH new_slots(slot_name) AS (
                VALUES(%s)
            )
            SELECT CASE WHEN slots.slot_name IS NULL THEN
                   pg_create_logical_replication_slot(new_slots.slot_name, %s)
                   ELSE NULL
                   END
            FROM new_slots
            LEFT JOIN (SELECT slot_name
                       FROM pg_replication_slots
                       WHERE slot_name = %s) slots
            ON slots.slot_name = new_slots.slot_name;
        """

        try:
            # must use separate connection as main replication connection
            # doesn't support the custom query
            with psycopg2.connect(self.dsn) as conn, conn.cursor() as cursor:
                cursor.execute(command, (self.slot, self.plugin, self.slot))
        except psycopg2.Error as e:
            logger.error(f'error creating replication slot: {e}')

    def is_slot_active(self):
        """
        Is the configured replication slot active?
        """
        command = """
            SELECT active
            FROM pg_replication_slots
            WHERE slot_name = %s;
        """

        with psycopg2.connect(self.dsn) as conn, conn.cursor() as cursor:
            cursor.execute(command, [self.slot])
            result = cursor.fetchone()

        return result is not None and result[0]

    def drop_slot(self):
        logger.info(f'dropping replication slot "{self.slot}"')

        command = """
            SELECT pg_drop_replication_slot(slot_name)
            FROM pg_replication_slots
            WHERE slot_name = %s;
        """
        dropped = False

        try:
            with psycopg2.connect(self.dsn) as conn, conn.cursor() as cursor:
                cursor.execute(command, [self.slot])
            dropped = True
        except Exception as e:
            logger.error(f'error dropping replication slot: {e}')

        return dropped

    def destroy(self, timeout=2.0):
        """
        Attempts to destroy the receiver by closing the DB connection and
        dropping the replication slot once it's become inactive.

        :param timeout: maximum time to wait for the slot to become inactive
        :return: True if slot was destroyed, False otherwise.
        """
        self.close()

        destroy_time = datetime.utcnow()
        # NB: there is a delay between the connection closing and the
        # replication slot becoming inactive and thus ready for deletion
        wait_time = timedelta(seconds=timeout)

        while self.is_slot_active() and destroy_time + wait_time > datetime.utcnow():
            time.sleep(0.1)

        return self.drop_slot()

    @classmethod
    def _get_include_tables(cls, config):
        includes_file = config.pop('includes_file', '')

        if includes_file:
            with open(includes_file) as inc_f:
                incs = inc_f.readline()
        else:
            incs = config.pop('includes', [])

        includes_extra = config.pop('includes_extra', '')
        if includes_extra:
            incs = f'{incs}, {includes_extra}' if incs else includes_extra

        if isinstance(incs, str):
            incs = [x.strip() for x in incs.replace('\n', '').split(',')]

        if not isinstance(incs, list):
            raise ConfigError(f'includes should be a list, got {incs}')

        return incs


class Wal2JsonReceiver(BaseReceiver):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Хранилище чанков сообщения
        self._message_chunks = []

        self.table_columns = {}

    @classmethod
    def from_config(cls, config):
        options = []
        # TODO: make them the same (parse the underscore version in the plugin)
        filtered_parameters = list(filter(lambda p: p in config, WAL2JSON_CONFIGURATION_PARAMETERS))

        for parameter_name in filtered_parameters:
            parameter_value = config.pop(parameter_name)

            options.append((parameter_name.replace('_', '-'), (parameter_value and 't' or 'f')))

        include_tables = cls._get_include_tables(config)

        if include_tables:
            options.append(('add-tables', ','.join(include_tables)))

        if config:
            raise ConfigError(f'unknown {cls.__name__} option entries: {", ".join(sorted(config))}')

        return cls(options=options)

    def process_payload(self, raw_payload):
        chunk = raw_payload.decode('utf-8')

        logger.debug(f'message received:\n\t{chunk}')

        self._message_chunks.append(chunk)

        # Последняя часть сообщения одной транзакции всегда равна ]}
        if not self.write_in_chunks or self.write_in_chunks and chunk == ']}':
            message = json.loads(''.join(self._message_chunks))

            del self._message_chunks[:]

            change = message['change']

            data = {
                'xid': message['xid'],
                'changes': [
                    {
                        'kind': item['kind'],  # update, insert, delete
                        'table': item['table'],
                        'key': (
                            item['oldkeys']['keyvalues'][0]
                            if 'oldkeys' in item
                            else None
                        ),
                        'record': (
                            dict(zip(item['columnnames'], item['columnvalues']))
                            if 'columnvalues' in item
                            else None
                        ),
                    }
                    for item in change
                ],
                'msg': message,
            }

            self.message_cb(data)


class JsonReceiver(BaseReceiver):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self._chunks = []
        self.table_columns = {}

    @classmethod
    def from_config(cls, config):
        opts = []
        # TODO: make them the same (parse the underscore version in the plugin)
        for k in ('pretty-print', 'include_xids', 'include_lsn',
                  'include_timestamp', 'include_schemas', 'include_types',
                  'include_empty_xacts'):
            if k in config:
                v = config.pop(k)
                opts.append((k.replace('_', '-'), (v and 't' or 'f')))

        incs = cls._get_include_tables(config)

        for inc in incs:
            if '.' in inc:
                schema, table = inc.split('.')
                item = {'schema': schema, 'table': table}
            else:
                item = {'table': inc}

            opts.append(('include', json.dumps(item)))

        excs = config.pop('excludes', [])
        if isinstance(excs, str):
            excs = [x.strip() for x in excs.split(',')]

        if not isinstance(excs, list):
            raise ConfigError(f'excludes should be a list, got {excs}')

        for exc in excs:
            item = {'table': exc}
            opts.append(('exclude', json.dumps(item)))

        if config:
            raise ConfigError(f'unknown {cls.__name__} option entries: {", ".join(sorted(config))}')

        # NOTE: it is currently necessary to write in chunk even if this
        # results in messages containing invalid JSON (which are assembled
        # by consume()). If we don't do so, it seems postgres fails to flush
        # the lsn correctly. I suspect the problem is that we reset the lsn
        # at the start of the message: if the output is chunked we receive
        # at least a couple of messages within the same transaction so we
        # end up being correct. If the message encompasses the entire
        # transaction, the lsn is reset at the beginning of the transaction
        # already seen, so some records are sent repeatedly.
        opts = [('write-in-chunks', '1')] + opts

        return cls(options=opts)

    def process_payload(self, raw_payload):
        chunk = raw_payload.decode('utf-8')

        logger.debug(f'message received:\n\t{chunk}')

        self._chunks.append(chunk)

        # attempt parsing each chunk as part of the whole
        try:
            obj = json.loads(''.join(self._chunks))
            del self._chunks[:]
            change = obj['tx']
            # сохраним колонки таблиц если они есть.
            # они приходят только первый раз
            for item in change:
                if ('colnames' in item and
                        item['table'] not in self.table_columns):
                    self.table_columns[item['table']] = item['colnames']

            data = {
                'xid': obj['xid'],
                'changes': [{
                    'kind': ACTIONS.get(item['op'], ''),
                    'table': item['table'],
                    'key': item['oldkey'][0] if 'oldkey' in item else None,
                    'record': dict(zip(self.table_columns[item['table']],
                                       item['values'])
                                   ) if 'values' in item else None,
                } for item in change],
                'msg': obj,
            }
            self.message_cb(data)
        except ValueError:
            pass
