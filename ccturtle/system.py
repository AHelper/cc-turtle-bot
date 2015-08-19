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


import tornado.log
from ccturtle.pathing import Pathing
from ccturtle.requestparser import RequestValidator
from ccturtle.turtle import Turtle
from ccturtle.plot import Plot
from ccturtle.building import Building
from ccturtle.sqlitestorage import SQLiteStorage
  
class System:
  def __init__(self):
    self.pathing = Pathing()
    self.turtles = {}
    self.validator = RequestValidator()
    self.storage = SQLiteStorage('/tmp/ccturtlesrv.db')
    
    names = self.storage.getAllTurtleNames()
    
    for name in names:
      self.turtles[name] = self.storage.loadTurtle(name)
      tornado.log.app_log.info("Loading turtle '{}'".format(name))
      
  def save(self):
    for turtle in self.turtles.itervalues():
      tornado.log.app_log.info("Saving {}".format(turtle.name))
      self.storage.saveTurtle(turtle)
    self.pathing.save()
    
  def addTurtle(self, turtle):
    self.turtles[turtle.getName()] = turtle
    
  def getTurtle(self, name):
    return self.turtles[name]
  
  def delTurtle(self, name):
    del self.turtles[name]
    self.storage.delTurtle(name)
  
  def hasTurtle(self, name):
    return self.turtles.has_key(name)
