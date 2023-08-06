# данная функция взята из
# https://github.com/transferwise/pipelinewise-tap-postgres/blob/master/tap_postgres/sync_strategies/logical_replication.py
def int_to_lsn(lsni):
    """Convert int to pg_lsn"""

    if not lsni or not isinstance(lsni, int):
        return None

    # Convert the integer to binary
    lsnb = f'{lsni:b}'

    # file is the binary before the 32nd character, converted to hex
    if len(lsnb) > 32:
        file = (format(int(lsnb[:-32], 2), 'x')).upper()
    else:
        file = '0'

    # index is the binary from the 32nd character, converted to hex
    index = (format(int(lsnb[-32:], 2), 'x')).upper()
    # Formatting
    lsn = f"{file}/{index}"

    return lsn
