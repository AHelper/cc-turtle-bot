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
from ccturtle.plot import Plot
from ccturtle.building import Building

class SQLiteStorageItem:
  def sql(self):
    raise NotImplementedError()
  
  @staticmethod
  def args(self):
    raise NotImplementedError()
  
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
    
    cur.execute("CREATE TABLE IF NOT EXISTS turtles (civ integer, name text, id integer PRIMARY KEY, x integer, y integer, z integer, facing integer)")
    cur.execute("CREATE TABLE IF NOT EXISTS civs (id integer primary key, name text)")
    cur.execute("CREATE TABLE IF NOT EXISTS buildings (id integer PRIMARY KEY, x integer, y integer, z integer, mk integer, building_type text)")
    cur.execute("CREATE TABLE IF NOT EXISTS plots (id integer PRIMARY KEY, x integer, y integer, z integer)")
    cur.execute("CREATE TABLE IF NOT EXISTS building_plots (bid integer, pid integer)")
    self.conn.commit()
    
  def getCursor(self):
    return self.conn.cursor()
  
  def commit(self):
    self.conn.commit()
    
  def rollback(self):
    self.conn.rollback()
  
  def __getAllIds(self, table):
    cur = self.conn.cursor()
    
    ids = []
    for row in cur.execute("SELECT id FROM {}".format(table)):
      ids.append(row[0])
    return ids
  
  def __load(self, varstr, table, id, type):
    cur = self.conn.cursor()
    
    cur.execute("SELECT {} FROM {} WHERE id = ?".format(varstr, table), id)
    
    row = cur.fetchone()
    
    if row != None:
      d = {}
      for i, key in enumerate(type.args()):
        d[key] = row[i]
      return type(**d)
    else:
      return None
    
  def __save(self, table, varstr, storage_item):
    cur = self.conn.cursor()
    
    cur.execute("INSERT OR REPLACE INTO {} ({}) VALUES ({})".format(table, varstr, ((varstr.count(",")+1)*"?,")[:-1]), storage_item.sql())
    
    self.conn.commit()
    
  def __del(self, table, storage_item):
    cur = self.conn.cursor()
    
    cur.execute("DELETE FROM {} WHERE id = ?".format(table), storage_item.sql()[0])
    
    self.conn.commit()
    
  def getAllTurtleNames(self):
    return self.__getAllIds("turtle")
  
  def loadTurtle(self, id):
    return self.__load("id, x, y, z, facing, name, designation, civ", "turtles", id, Turtle)
  
  def saveTurtle(self, turtle):
    self.__save("turtles", "id, x, y, z, facing, name, designation, civ", turtle)
    
  def delTurtle(self, id):
    self.__del("turtles", id)
  
  def getAllPlotIds(self):
    return self.__getAllIds("plots")
  
  def loadPlot(self, id):
    self.__load("id, x, y, z", "plots", id, Plot)
    
  def savePlot(self, plot):
    self.__save("plots", "id, x, y, z", plot)
    
  def delPlot(self, plot):
    self.__del("plots", plot)
    
  def getAllBuildingIds(self):
    return self.__getAllIds("buildings")
  
  def loadBuilding(self, id):
    return self.__load("id, x, y, z, building_type, mk", "buildings", id, Building)
  
  def saveBuilding(self, building):
    self.__save("buildings", "id, x, y, z, building_type, mk", building)
    
  def delBuilding(self, building):
    self.__del("building", building)
  
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
