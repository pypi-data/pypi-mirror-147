CONFIG_FILE = '/etc/rvr/config.ini'

LOG_TYPE_APPLICATION_EVENT = 'app_event'

VALID_MESSAGE_TYPES = {'debug', 'info', 'warning', 'error'}

NOTIFY_APPLICATION_EVENT = '{type} on {node}: {message}'

# Messages
MSG_POST_DATA_SUCCESS = 'Accepted payload: {body}'

# Errors:
ERR_POST_DATA = 'Unable to Write: {status_code}'
