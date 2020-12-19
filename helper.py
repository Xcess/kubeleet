#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from configparser import SafeConfigParser
import logging


class Config(SafeConfigParser):
    """Config Module"""

    def __init__(self, path="/etc/kubeleet.conf"):
        super(Config, self).__init__()
        self.path = path
        self.read(self.path)


CONF = Config("./kubeleet.conf")

logging.basicConfig(
    format="[%(levelname)s] %(asctime)s  %(message)s",
    datefmt="%m/%d/%Y %H:%M:%S",
    level=logging.INFO if CONF.getboolean("general", "verbose") else logging.WARN,
)


log = logging.info
crit = logging.critical
