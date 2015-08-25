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


from tornado.web import HTTPError
from ccturtle.server.json import JSONHandler

class GoalsListHandler(JSONHandler):
  def initialize(self, sys, resolver, validator):
    self.resolver = resolver
    self.validator = validator
    
  def get(self):
    # TODO
    pass
  
class GoalsAddHandler(JSONHandler):
  def initialize(self, sys, resolver, validator):
    self.resolver = resolver
    self.validator = validator
    
  def post(self):
    req = self.read_json()
    if not self.validator.validate(GoalsAddHandler, req):
      raise HTTPError(400)
    else:
      # TODO
      pass
  
class GoalsRemoveHandler(JSONHandler):
  def initialize(self, sys, resolver, validator):
    self.resolver = resolver
    self.validator = validator
    
  def post(self):
    req = self.read_json()
    if not self.validator.validate(GoalsRemoveHandler, req):
      raise HTTPError(400)
    else:
      # TODO
      pass
