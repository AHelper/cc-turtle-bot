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


import sqlite3
import tornado.log
from ccturtle.pathing import Pathing
from ccturtle.requestparser import RequestValidator
from ccturtle.turtle import Turtle

class SQLiteStorage:
  def __init__(self, path):
    self.path = path
    self.__open()
    self.__createTables()
    self.__close()
    self.__open()
  
  def __open(self):
    self.conn = sqlite3.connect(self.path)
    
  def __close(self):
    self.conn.commit()
    self.conn.close()
    
  def __createTables(self):
    cur = self.conn.cursor()
    
    cur.execute("CREATE TABLE IF NOT EXISTS turtles (civ integer, name text PRIMARY KEY, x integer, y integer, z integer, facing integer)")
    cur.execute("CREATE TABLE IF NOT EXISTS civs (id integer, name text)")
    self.conn.commit()
    
  def loadTurtle(self, id):
    cur = self.conn.cursor()
    
    cur.execute("SELECT name, x, y, z, facing FROM turtles WHERE name=?", (id,))
    
    row = cur.fetchone()
    
    if row != None:
      return Turtle(row[0], int(row[1]), int(row[2]), int(row[3]), int(row[4]))
    else:
      return None
    
  def delTurtle(self, id):
    cur = self.conn.cursor()
    
    cur.execute("DELETE FROM turtles WHERE name=?", id)
    
    self.conn.commit()
  
  def saveTurtle(self, turtle):
    cur = self.conn.cursor()
    
    cur.execute("INSERT OR REPLACE INTO turtles (civ, name, x, y, z, facing) VALUES (?,?,?,?,?,?)",(
                0,
                turtle.name,
                turtle.x,
                turtle.y,
                turtle.z,
                turtle.facing))
    self.conn.commit()
  
  def getAllTurtleNames(self):
    cur = self.conn.cursor()
    
    names = []
    for row in cur.execute("SELECT name FROM turtles"):
      names.append(row[0])
    return names
  
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
