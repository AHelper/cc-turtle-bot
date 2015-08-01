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


'''
Documentation, License etc.

@package turtlesim
'''


class Range:
  MAX_VALUE = 9999
  def __init__(self, key, value):
    self.value = value
    
    if type(key) == int:
      # absolute
      self.min = self.max = key
    elif type(key) == str:
      parts = key.split('..')
      
      if len(parts) != 2:
        raise KeyError()
      
      if len(parts[0]) == 0:
        self.min = 0
      else:
        self.min = int(parts[0])
      
      if len(parts[1]) == 0:
        self.max = self.MAX_VALUE
      else:
        self.max = int(parts[1])
  
  def getMin(self):
    return self.min
  
  def getMax(self):
    return self.max
  
  def getValue(self):
    return self.value
  
class goal:
  def __init__(self,yml):
    self.yml = yml
    self.goals = []
    self.actions = []
    self.any = []
    self.free = []
    self.idle = []
    self.triggers = []
    
    # Check if yaml is map
    if type(yml) != dict:
      raise AttributeError()
    
    if not yml.has_key('id'):
      raise AttributeError()
    else:
      self.id = yml['id']
    
    if not yml.has_key('priority'):
      self.priority = 5
    else:
      self.priority = int(yml['priority'])
    
    if yml.has_key('requires'):
      if type(yml['requires']) == dict:
        req = yml['requires']
        
        if req.has_key('goals'):
          self.goals = req['goals']
        if req.has_key('actions'):
          self.actions = req['actions']
        if req.has_key('any'):
          self.any = self.processRangeMap(req['any'])
        if req.has_key('free'):
          self.free = self.processRangeMap(req['any'])
        if req.has_key('idle'):
          self.idle = self.processRangeMap(req['idle'])
          
    if yml.has_key('triggers'):
      self.triggers = yml['triggers']
    
    # Validate variables

class building_annotation:
  def __init__(self,yml):
    self.yml = yml
    self.pos = [0,0,0]
    self.type = None
    self.metadata = dict()
    
    if yml.has_key('pos'):
      self.pos = [int(x) for x in yml['pos'].split(' ')]
    if yml.has_key('type'):
      self.type = yml['type']
    if yml.has_key('metadata') and type(yml['metadata']) == dict:
      self.metadata = yml['metadata']
      
class building:
  def __init__(self,yml):
    self.yml = yml
    
    if type(yml) != dict:
      raise AttributeError()
    
    if not yml.has_key('id'):
      raise AttributeError()
    else:
      self.id = yml['id']
    
    if yml.has_key('schematic'):
      self.schematic = yml['schematic']
    if yml.has_key('size'):
      self.size = [int(x) for x in yml['size'].split('x')]
    if yml.has_key('type'):
      self.type = yml['type']
    if yml.has_key('annotations') and type(yml['annotations']) == dict:
      ann = yml['annotations']
      
      self.annotations = [building_annotation(a) for a in ann]
    if yml.has_key('provides'):
      self.provides = yml['provides']
    if yml.has_key('next'):
      self.next = yml['next']
    if yml.has_key('prev'):
      self.prev = yml['prev']
    
class unit:
  def __init__(self, yml):
    self.yml = yml
    
    if type(yml) != dict:
      raise AttributeError()
    
class action:
  def __init__(self, id, args):
    self.id = id
    self.args = args