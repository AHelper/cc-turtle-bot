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
    
class RegisterTurtleHandler(JSONHandler):
  def initialize(self, sys, resolver, validator):
    self.sys = sys
    self.validator = validator
    
  def post(self, name):
    req = self.read_json()
    if not self.validator.validate(RegisterTurtleHandler, req):
      print("Failed to validate")
      raise HTTPError(400)
    
    if not self.sys.hasTurtle(name):
      self.sys.addTurtle(Turtle(name, req['x'], req['y'], req['z'], req['facing']))
      self.write_json({"type":"success"})
    else:
      self.write_json({"type":"failure","message":"turtle alread exists"})
      
class UnregisterTurtleHandler(JSONHandler):
  def initialize(self, sys, resolver, validator):
    self.sys = sys
    
  def post(self, name):    
    if not self.sys.hasTurtle(name):
      self.sys.delTurtle(name)
      self.write_json({"type":"success"})
    else:
      self.write_json({"type":"failure","message":"turtle alread exists"})
      
class TurtleStatusHandler(JSONHandler):
  def initialize(self, sys, resolver, validator):
    self.sys = sys
    
  def get(self, turtle_name):
    if not self.sys.hasTurtle(turtle_name):
      raise HTTPError(404)
    else:
      self.write_json({"type":"success","current":self.sys.getTurtle(turtle_name).getHumanReadableCurrentTask(),"future":self.sys.getTurtle(turtle_name).getHumanReadableFutureTasks()})

class TurtleActionHandler(JSONHandler):
  def initialize(self, sys, resolver, validator):
    self.sys = sys
    
  def get(self, id):
    if not self.sys.hasTurtle(id):
      raise HTTPError(404)
    else:
      self.write_json({"type":"success","action":self.sys.getTurtle(id).getCurrentTaskInfo()["action"],"data":self.sys.getTurtle(id).getCurrentTaskInfo()["data"]})
      
class TurtlePositionHandler(JSONHandler):
  def initialize(self, sys, resolver, validator):
    self.sys = sys
    self.validator = validator
    
  def get(self, id):
    if not self.sys.hasTurtle(id):
      raise HTTPError(404)
    else:
      t = self.sys.getTurtle(id)
      self.write_json(t.getPosition())
  def post(self, id):
    if not self.sys.hasTurtle(id):
      raise HTTPError(404)
    else:
      req = self.read_json()
      if not self.validator.validate(TurtlePositionHandler, req):
        raise HTTPError(400)
      else:
        t = self.sys.getTurtle(id)
        t.setPosition(req["x"],req["y"],req["z"],req["facing"])
        self.write_json({"type":"success"})
        
class TurtleGetActionHandler(JSONHandler):
  def initialize(self, sys, resolver, validator):
    self.resolver = resolver
    self.sys = sys
  
  def get(self, id):
    if not self.sys.hasTurtle(id):
      raise HTTPError(404)
    else:
      t = self.sys.getTurtle(id)
      rpc = self.resolver.getAction(t)
      
      if rpc:
        self.write_json(rpc)
      else:
        raise HTTPError(203) # No content
      
class TurtleResponseHandler(JSONHandler):
  def initialize(self, sys, resolver, validator):
    self.resolver = resolver
    self.sys = sys
    self.validator = validator
    
  def post(self, id):
    if not self.sys.hasTurtle(id):
      raise HTTPError(404)
    else:
      req = self.read_json()
      t = self.sys.getTurtle(id)
      # Don't use the validator, JSON-RPC has special rules
      # GOAP should handle it
      self.resolver.handleReply(t, req)
      self.write_json({"type":"success"})