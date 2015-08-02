#!/usr/bin/python

# cc-turtle-bot
# Copyright (C) 2015 Collin Eggert
# 
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# 
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.


from __future__ import absolute_import
import logging
import tornado.log
from ccturtle.server.json import JSONHandler
    
class LoggingHandler(JSONHandler):
  def initialize(self, sys):
    self.sys = sys
    
  def post(self, id, level):
    level = int(level)
    tornado.log.app_log.setLevel(logging.DEBUG)
    if level <= 2:
      tornado.log.app_log.critical("{}: {}".format(id,self.request.body))
    elif level == 3:
      tornado.log.app_log.error("{}: {}".format(id,self.request.body))
    elif level == 4:
      tornado.log.app_log.warning("{}: {}".format(id,self.request.body))
    elif level == 5 or level == 6:
      tornado.log.app_log.info("{}: {}".format(id,self.request.body))
    elif level == 7:
      tornado.log.app_log.debug("{}: {}".format(id,self.request.body))