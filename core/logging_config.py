import logging
import logging.config
from pathlib import Path
from datetime import datetime
from flask import g, has_request_context

class RequestIdFilter(logging.Filter):

    def filter(self, record):

        if has_request_context():
            record.request_id = getattr(
                g,
                "request_id",
                "no-request-id"
            )
        else:
            record.request_id = "system"

        return True
    

def setup_logging():
    Path('logs').mkdir(parents=True, exist_ok=True)
    file_name = datetime.now().strftime("logs/log_%Y%m%d.log")
    logging_config = {
        'version': 1,
        'disable_existing_loggers': False,
        'formatters': {
            'default': {
                'format': '[%(asctime)s] %(levelname)s [%(request_id)s] [%(name)s]: %(message)s.', # Otros parametros que no se incluyen porque afecta el resultado cuando se usa un decorador para el logger: [%(module)s in %(pathname)s:%(lineno)d] 
            },
        },
        'filters': {
            'request_id': {
                '()': RequestIdFilter,
            },
        },
        'handlers': {
            'console': {
                'class': 'logging.StreamHandler',
                'formatter': 'default',
                'level': logging.DEBUG,
                'filters': ['request_id'],
            },
            'file': {
                'class': 'concurrent_log_handler.ConcurrentRotatingFileHandler',
                #'class': 'logging.handlers.RotatingFileHandler',
                'filename': file_name,
                'formatter': 'default',
                'level': logging.DEBUG,
                'maxBytes': 1024*1024*2,  # 2 MB
                'backupCount': 3,  # Mantener los últimos 3 archivos de log
                'encoding': 'utf-8',
                #'errors': 'ignore',
                'filters': ['request_id'],
            },
            'werkzeug_file': {
                'class': 'concurrent_log_handler.ConcurrentRotatingFileHandler',
                #'class': 'logging.handlers.RotatingFileHandler',
                'filename': file_name,
                'formatter': 'default',
                'level': logging.INFO,
                'maxBytes': 1024*1024*2,
                'backupCount': 3,
                'encoding': 'utf-8',
                'filters': ['request_id'],
            },
        },
        'root': {
            'handlers': ['console', 'file'],
            'level': logging.DEBUG,
        },
        'loggers': {
            'werkzeug': {
                'handlers': ['console', 'werkzeug_file'],
                'level': logging.DEBUG,
                'propagate': False,  # Evitar que los logs de Werkzeug se propaguen al logger raíz
            },
            # 'sqlalchemy.engine': {
            #     'handlers': ['console', 'file'],
            #     'level': logging.INFO,  # Cambiar a INFO para reducir el nivel de detalle de los logs de SQLAlchemy
            #     'propagate': False,  # Evitar que los logs de SQLAlchemy se propaguen al logger raíz
            # },

        },
    }
    logging.config.dictConfig(logging_config)



