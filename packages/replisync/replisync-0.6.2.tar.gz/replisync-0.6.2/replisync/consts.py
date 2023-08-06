ACTIONS = {'U': 'update', 'I': 'insert', 'D': 'delete'}

WRITE_IN_CHUNKS = 'write-in-chunks'

WAL2JSON_CONFIGURATION_PARAMETERS = (
    'pretty-print',
    WRITE_IN_CHUNKS,
    'include_xids',
    'include-lsn',
    'include_timestamp',
    'include-schemas',
    'include-types',
    'include-empty-xacts',
)
