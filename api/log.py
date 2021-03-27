import logging
import warnings
import logging
# NEeds to be here to configure airflow logging first
from airflow import logging_config

log_config = dict(
    format="%(asctime)s %(levelname)-6s %(name)-25s %(funcName)-20s %(message)s",
    level=logging.CRITICAL,
    datefmt="%Y-%m-%dT%H:%M:%S",
)


class NoParsingFilter(logging.Filter):
    def filter(self, record):
        return not record.getMessage().startswith('BMB')


for name in logging.Logger.manager.loggerDict.keys():
    log = logging.getLogger(name)
    log.setLevel(logging.CRITICAL)
    log.addFilter(NoParsingFilter())


warnings.filterwarnings("ignore")
warnings.simplefilter("ignore")

logging.basicConfig(**log_config)

logger = logging
