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
from ccturtle.goap.goap import GoalResolver
from ccturtle.requestparser import RequestValidator

class GoalsListHandler(JSONHandler):
  def initialize(self, sys, resolver, validator):
    self.resolver = resolver
    self.validator = validator
    
    assert isinstance(self.resolver, GoalResolver)
    assert isinstance(self.validator, RequestValidator)
    
  def get(self):
    def childGoalsToNames(goal):
      remap = {}
      for key in goal.iterkeys():
        remap[key.name] = childGoalsToNames(goal[key])
      return remap
    
    goals = {
      "all": [goal.name for goal in self.resolver.getAllGoals()],
      "active": childGoalsToNames(self.resolver.getGoals())
    }
    
    self.write_json(goals)
  
class GoalsAddHandler(JSONHandler):
  def initialize(self, sys, resolver, validator):
    self.resolver = resolver
    self.validator = validator
    
    assert isinstance(self.resolver, GoalResolver)
    assert isinstance(self.validator, RequestValidator)
    
  def post(self):
    req = self.read_json()
    if not self.validator.validate(GoalsAddHandler, req):
      raise HTTPError(400)
    else:
      for goal in self.resolver.getAllGoals():
        if goal.name == req["goal"]:
          self.resolver.doGoal(goal)
          self.write_json({"type":"success"})
          return
      raise HTTPError(404)
  
class GoalsRemoveHandler(JSONHandler):
  def initialize(self, sys, resolver, validator):
    self.resolver = resolver
    self.validator = validator
    
    assert isinstance(self.resolver, GoalResolver)
    assert isinstance(self.validator, RequestValidator)
    
  def post(self):
    req = self.read_json()
    if not self.validator.validate(GoalsRemoveHandler, req):
      raise HTTPError(400)
    else:
      raise NotImplementedError()
