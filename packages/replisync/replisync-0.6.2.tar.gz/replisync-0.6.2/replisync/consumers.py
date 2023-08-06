import json
import logging
import os
import pickle
import uuid

from celery import (
    Celery,
)

from replisync.errors import (
    ConfigError,
)


logger = logging.getLogger('replisync')


class BaseConsumer:
    def __init__(self, conf=None):
        pass

    @classmethod
    def from_config(cls, opt):
        config = opt.get('config')
        return cls(conf=config)

    def stop(self):
        pass


class Printer(BaseConsumer):
    """
    Print the data received on stdout.
    """

    def process(self, msg):
        if isinstance(msg, str):
            logger.debug(msg)
        else:
            logger.debug(json.dumps(msg))


class CeleryConsumer(BaseConsumer):

    def __init__(self, conf=None):
        super().__init__(conf)
        broker = conf.get('replisync', 'celery_broker_url')
        if not broker:
            raise ConfigError('Celery broker not configure')

        # подключаемся к очереди задач
        self.celery_app = Celery('tasks', broker=broker)
        default_key = conf.get('replisync', 'task_default_routing_key')
        default_queue = conf.get('replisync', 'task_default_queue')
        self.celery_app.conf.task_default_routing_key = default_key
        self.celery_app.conf.task_default_queue = default_queue
        self.taskname = conf.get('replisync', 'task')
        self.system = conf.get('replisync', 'system', fallback='')
        self.routing = self.parse_routing(conf)
        self.output_dir = conf.get('replisync', 'output_dir')
        if self.output_dir:
            self.output_dir = self.output_dir.rstrip('/')
            if not os.path.isdir(self.output_dir):
                raise ConfigError(f'directory {self.output_dir} it does not exist')

    def process(self, msg):
        changes = msg['changes']
        xid = msg['xid']

        # пихаем в очередь информацию об изменившейся записи
        if changes:
            queue = self.get_queue(changes)
            # system - система
            # xid - транзакция
            # changes
            #   table - таблица
            #   kind - действие U, update
            #   key - ключ
            #   record - запись
            params = {
                'system': self.system,
                'xid': xid,
                'changes': changes,
            }

            logger.info(
                f'Send task "{self.taskname}" to queue: {queue if queue else self.taskname} '
                f'with params {params}'
            )

            if self.output_dir:
                # Параметр 'changes' записывается в файл, а не передается в очередь напрямую
                file_path = f'{self.output_dir}/{self.system}_{uuid.uuid4()}'
                pickle.dump(params, open(file_path, 'wb'), protocol=pickle.HIGHEST_PROTOCOL)
                params['changes'] = []
                params.update({'file_with_params': file_path})

            self.celery_app.send_task(
                self.taskname, args=[], kwargs=params, queue=queue
            )

            if isinstance(changes, str):
                logger.debug(changes)
            else:
                logger.debug(json.dumps(changes))

    def stop(self):
        super().stop()

    @staticmethod
    def parse_routing(conf) -> dict:
        """
        Разбор секции routing файла настроек и подготовка словаря маршрутизации.
        В секции [routing] настройки представлены так:
            имя_очереди = список,таблиц,разделенный,запятыми
        Args:
            conf: ConfigParser, загруженный файл настроек сервиса

        Returns: словарь маршрутизакции вида "имя таблицы": "имя очереди"
        """
        result = {}

        for queue, value in conf.items('routing'):
            for table_name in (value or '').split(','):
                table_name = table_name.strip()
                if table_name not in result:
                    result[table_name] = queue

        return result

    def get_queue(self, changes: dict) -> str:
        """
        Определение очередь для задачи по наличию изменений по таблицам
        Args:
            changes: список изменений

        Returns: очередь задачи или None, если не определено
        """
        queue = None

        if self.routing:
            # ищем первую таблицу, которая подойдет под настройки маршрутизации
            for change in changes:
                queue = self.routing.get(change['table'], None)
                if queue:
                    break

        return queue
