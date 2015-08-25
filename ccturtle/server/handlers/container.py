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
from ccturtle.turtle import Turtle
from ccturtle.server.json import JSONHandler

class ContainerGetHandler(JSONHandler):
  def initialize(self, sys, resolver, validator):
    self.sys = sys
    self.validator = validator
    
  def post(self):
    req = self.read_json()
    if not self.validator.validate(ContainerGetHandler, req):
      raise HTTPError(400)
    else:
      # TODO
      pass
      
class ContainerPutHandler(JSONHandler):
  def initialize(self, sys, resolver, validator):
    self.sys = sys
    self.validator = validator
    
  def post(self, id):
    if int(id) not in self.sys.containers:
      raise HTTPError(404)
    else:
      req = self.read_json()
      if not self.validator.validate(ContainerPutHandler, req):
        raise HTTPError(400)
      else:
        # TODO
        pass
      
class ContainerTakeHandler(JSONHandler):
  def initialize(self, sys, resolver, validator):
    self.sys = sys
    self.validator = validator
    
  def post(self, id):
    if int(id) not in self.sys.containers:
      raise HTTPError(404)
    else:
      req = self.read_json()
      if not self.validator.validate(ContainerPutHandler, req):
        raise HTTPError(400)
      else:
        # TODO
        pass
      
class ContainerClearHandler(JSONHandler):
  def initialize(self, sys, resolver, validator):
    self.sys = sys
    self.validator = validator
    
  def get(self, id):
    if int(id) not in self.sys.containers:
      raise HTTPError(404)
    else:
      # TODO
      pass
      
class ContainerSetHandler(JSONHandler):
  def initialize(self, sys, resolver, validator):
    self.sys = sys
    self.validator = validator
    
  def post(self, id):
    if int(id) not in self.sys.containers:
      raise HTTPError(404)
    else:
      req = self.read_json()
      if not self.validator.validate(ContainerPutHandler, req):
        raise HTTPError(400)
      else:
        # TODO
        pass