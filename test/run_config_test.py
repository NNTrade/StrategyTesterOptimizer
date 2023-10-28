import unittest
import logging
from src.strategy.run_config.run_config_set import RunConfigSet
from src.strategy.run_config.run_config import date


class RunConfig_TestCase(unittest.TestCase):

    logger = logging.getLogger(__name__)
    logging.basicConfig(format='%(asctime)s %(module)s %(levelname)s: %(message)s',
                        datefmt='%m/%d/%Y %I:%M:%S %p', level=logging.INFO)

    