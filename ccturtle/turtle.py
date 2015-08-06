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


"""
Control entrypoint for a single turtle.
"""
class Turtle:
  BUILDER = 1
  MINER = 2
  CRAFTER = 4
  FORRESTER = 8
  FARMER = 0x10
  
  def __init__(self, unique_name, x, y, z, facing):
    self.x = x
    self.y = y
    self.z = z
    self.facing = facing
    self.name = unique_name
    
    self.designation = None
  
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
    pass
  
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
    pass
  
  def getCurrentTaskInfo(self):
    pass
  
  def getHumanReadableCurrentTask(self):
    return "Faffing about"
  
  def getHumanReadableFutureTasks(self):
    return "More faffing about"
  