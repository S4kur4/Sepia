#!/usr/bin/env python
#-*- coding:utf-8 -*-

import ConfigParser
from lib.core.data import paths, logger
from lib.core.common import getSafeExString


class ConfigFileParser:
    @staticmethod
    def _get_option(section, option):
        try:
            cf = ConfigParser.ConfigParser()
            cf.read(paths.CONFIG_PATH)
            return cf.get(section=section, option=option)
        except ConfigParser.NoOptionError, e:
            logger.warning('Missing essential options, please check your config-file')
            logger.error(getSafeExString(e))
            return ''

    def ZoomEyeEmail(self):
        return self._get_option('zoomeye', 'email')

    def ZoomEyePassword(self):
        return self._get_option('zoomeye', 'password')

    def UrlFilter(self):
        return self._get_option('urlfilter', 'regex')
