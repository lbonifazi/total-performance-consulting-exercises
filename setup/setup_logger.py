import logging

from setup.setup_app import LOGS_FILE_PATH

logging.basicConfig(filename='{}/total_performance.log'.format(LOGS_FILE_PATH), level=logging.DEBUG,
                    format='%(asctime)s %(levelname)s %(name)s %(message)s')
logger = logging.getLogger(__name__)
