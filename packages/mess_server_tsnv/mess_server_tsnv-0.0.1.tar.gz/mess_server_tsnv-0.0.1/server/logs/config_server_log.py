import sys
import os

from logging import StreamHandler, INFO, getLogger, handlers

from common.variables import ENCODING, LOGGING_LEVEL

sys.path.append('../')

# создаём формировщик логов (formatter):
server_formatter = logging.Formatter('%(asctime)s %(levelname)s %(filename)s %(message)s')

# Подготовка имени файла для логирования
path = os.path.dirname(os.path.abspath(__file__))
path = os.path.join(path, 'server.log')

# создаём потоки вывода логов
steam = StreamHandler(sys.stderr)
steam.setFormatter(server_formatter)
steam.setLevel(INFO)
log_file = handlers.TimedRotatingFileHandler(path, encoding=ENCODING, interval=1, when='D')
log_file.setFormatter(server_formatter)

# создаём регистратор и настраиваем его
logger = getLogger('server')
logger.addHandler(steam)
logger.addHandler(log_file)
logger.setLevel(LOGGING_LEVEL)

# отладка
if __name__ == '__main__':
    logger.critical('Test critical event')
    logger.error('Test error ivent')
    logger.debug('Test debug ivent')
    logger.info('Test info ivent')
