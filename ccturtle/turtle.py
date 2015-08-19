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


from ccturtle.sqlitestorage import SQLiteStorageItem

def designationToStr(designation):
  if designation == Turtle.MINER:
    return "miner"
  elif designation == Turtle.CRAFTER:
    return "crafter"
  elif designation == Turtle.FORRESTER:
    return "forrester"
  elif designation == Turtle.FARMER:
    return "farmer"
  elif designation == Turtle.BUILDER:
    return "builder"
"""
Control entrypoint for a single turtle.
"""
class Turtle(SQLiteStorageItem):
  MINER =     0x01
  CRAFTER =   0x02
  FORRESTER = 0x04
  FARMER =    0x08
  BUILDER =   MINER | FORRESTER | FARMER
  
  
  def __init__(self, unique_name, x, y, z, facing, id=None, civ=None, designation=None):
    self.x = x
    self.y = y
    self.z = z
    self.facing = facing
    self.name = unique_name
    self.civ = civ
    self.designation = designation
    self.id = id
    
  def sql(self):
    return (self.id, self.x, self.y, self.z, self.facing, self.name, self.designation, self.civ)
  
  @staticmethod
  def args(self):
    return "id x y z facing unique_name designation civ".split(" ")
  
  def getName(self):
    return self.name
  
  def setDesignation(self, designation):
    self.designation = designation
    
  def getDesignation(self):
    return self.designation
  
  def think(self):
    """
    Figures out what to do
    """
    pass
  
  def handleResponse(self, response):
    """
    Handles a response from the Lua code
    """
    if self.currentGoal:
      return self.currentGoal.handleReply(self, response)
    else:
      return None
  
  def setPosition(self, x, y, z, facing):
    self.x = x
    self.y = y
    self.z = z
    self.facing = facing
    
  def getPosition(self):
    return {
      "x":self.x,
      "y":self.y,
      "z":self.z,
      "facing":self.facing
    }
  
  def getResponse(self):
    """
    Generates a response for the turtle for what it should do
    """
    if self.currentGoal:
      return self.currentGoal.getResponse(self)
    else:
      return None
  
  def getCurrentTaskInfo(self):
    pass
  
  def getHumanReadableCurrentTask(self):
    return "Faffing about"
  
  def getHumanReadableFutureTasks(self):
    return "More faffing about"
  
  def setGoal(self, goal):
    self.currentGoal = goal
    
  def getGoal(self, goal):
    return self.currentGoal