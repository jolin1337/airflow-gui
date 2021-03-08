import logging

logging.basicConfig(
    format="%(asctime)s %(levelname)-6s %(name)-25s %(funcName)-20s %(message)s",
    level=logging.INFO,
    datefmt="%Y-%m-%dT%H:%M:%S",
)
logging.getLogger("matplotlib").setLevel(logging.WARNING)

logger = logging
