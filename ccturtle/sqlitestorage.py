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
    
    cur.execute("CREATE TABLE IF NOT EXISTS turtles (civ integer, name text, id integer PRIMARY KEY, x integer, y integer, z integer, facing integer, designation integer)")
    cur.execute("CREATE TABLE IF NOT EXISTS civs (id integer primary key, name text)")
    cur.execute("CREATE TABLE IF NOT EXISTS buildings (id integer PRIMARY KEY, x integer, y integer, z integer, mk integer, building_type text)")
    cur.execute("CREATE TABLE IF NOT EXISTS plots (id integer PRIMARY KEY, x integer, y integer, z integer)")
    cur.execute("CREATE TABLE IF NOT EXISTS building_plots (bid integer, pid integer)")
    cur.execute("CREATE TABLE IF NOT EXISTS variables (key text primary key, type text, value blob)")
    
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
    
    cur.execute("SELECT {} FROM {} WHERE id = ?".format(varstr, table), (id,))
    
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
    storage_item.id = cur.lastrowid
    
    self.conn.commit()
    
  def __del(self, table, storage_item):
    cur = self.conn.cursor()
    
    cur.execute("DELETE FROM {} WHERE id = ?".format(table), storage_item.sql()[0])
    
    self.conn.commit()
    
  def getAllTurtleIds(self):
    return self.__getAllIds("turtles")
  
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
    
  def saveVariable(self, key, value, type):
    cur = self.conn.cursor()
    
    cur.execute("INSERT OR UPDATE INTO variables (key, value, type) VALUES (?,?,?)", (key, value, type))
    
    self.conn.commit()
  
  def loadVariable(self, key):
    cur = self.conn.cursor()
    
    cur.execute("SELECT value, type FROM variables WHERE key = ?", key)
    
    row = cur.fetchone()
    
    if row != None:
      return (row[0], row[1])
    else:
      return None
    
  def delVariable(self, key):
    cur = self.conn.cursor()
    
    cur.execute("DELETE FROM variables WHERE key = ?", (key,))
    
    self.conn.commit()