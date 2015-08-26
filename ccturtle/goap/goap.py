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


#!/usr/bin/env python

import copy
import re
from ccturtle.turtle import Turtle, designationToStr
from ccturtle.system import SQLiteStorage
from ccturtle.pathing import Pathing

from yaml import load, load_all, dump, dump_all
try:
  from yaml import CLoader as Loader, CDumper as Dumper
except:
  from yaml import Loader, Dumper
  
# Temporary helper method, move to something more elegant in the future
rpc_call_id = 0
def genRPCCall(action_name, parameters):
  global rpc_call_id
  rpc_call_id += 1
  return {"action":action_name, "parameters":parameters, "id":rpc_call_id}

class Variables:
  def __init__(self, sys):
    assert isinstance(sys, System)
    self.items = {}
    self.plotscache = {}
    self.sys = sys
    
  def __iter__(self):
    return self.items.__iter__()
  
  def __contains__(self, item):
    return item in self.items
    
  def __getitem__(self, key):
    if not isinstance(key, str):
      raise KeyError(key)
    else:
      try:
        parts = key.split(".")
        assert len(parts) > 0, "bad key"
        
        if key in self.items:
          return self.items[key]
        elif parts[0] == "plots":
          wx = int(parts[1])
          wz = int(parts[2])
          i = (wx, wz)
          v = PlotsVariable(self.sys, wx, wz)
          self.items[v.name] = v
          return v
        elif parts[0] == "buildings":
          for b in self.sys.BUILDING_TYPES:
            if b[0] == parts[1]:
              mk = None
              free = False
              if len(parts) > 2:
                try:
                  mk = int(parts[2])
                  if mk > b[1]:
                    raise KeyError("Mk {} is too high for {} ({} max)".format(mk, b[0], b[1]))
                  del parts[2]
                except ValueError:
                  pass
              if len(parts) > 2:
                if parts[2] == "free":
                  free = True
              return BuildingsVariable(b[0], mk, free)
        else:
          raise KeyError()
      except:
        raise KeyError(key)
    
  def __setitem__(self, key, value):
    self.items[key] = value
    
  def __delitem__(self, key):
    del self.items[key]
        
  def iteritems(self):
    return self.items.iteritems()
  
  def itervalues(self):
    return self.items.itervalues()
  
  def iterkeys(self):
    return self.items.iterkeys()

class System:
  MAX_PLOT_DIM = 4
  BUILDING_TYPES = [
    ("mine",1),
    ("house",1)
  ]
  
  def __init__(self, path):
    self.turtles = {}
    self.claims = dict()
    self.variables = Variables(self)
    self.plots = {}
    self.sizedplotcache = {}
    self.buildings = {} # key -> (building name, mk)
    self.containers = {}
    self.pathing = Pathing() # TODO: Add in a path for the octrees
    # TODO, integrate SQL Storage
    self.sql = SQLiteStorage(path) 
    
    plotIds = self.sql.getAllPlotIds()
    for plotId in plotIds:
      plot = self.sql.loadPlot(plotId)
      self.plots[plotId] = plot
      
    buildingIds = self.sql.getAllBuildingIds()
    for buildingId in buildingIds:
      building = self.sql.loadBuilding(buildingId)
      self.buildings[buildingId] = building
    
    turtleIds = self.sql.getAllTurtleIds()
    for turtleId in turtleIds:
      turtle = self.sql.loadTurtle(turtleId)
      self.turtles[turtleId] = turtle
    
    containerIds = self.sql.getAllContainerIds()
    for containerId in containerIds:
      container = self.sql.loadContainer(containerId)
      self.containers[containerId] = container
    
  def __updateplotcache(self):
    # This is going to be bad for performance...
    self.sizedplotcache = {}
    for pos in self.plots.iterkeys():
      for oz in range(0,self.MAX_PLOT_DIM):
        for ox in range(0, self.MAX_PLOT_DIM):
          o = (pos[0]+ox, pos[1]+oz)
          if o in self.plots:
            i = (ox+1,oz+1)
            if i not in self.sizedplotcache:
              self.sizedplotcache[i] = []
            self.sizedplotcache[i].append(o)
      #ox = 1
      #oz = 0
      #while True:
        #if o not in self.plots:
          #break
        #self.sizedplotcache[
        
  def save(self):
    for building in self.buildings.itervalues():
      self.sql.saveBuilding(building)
    for plot in self.plots.itervalues():
      self.sql.savePlot(plot)
    for turtle in self.turtles.itervalues():
      self.sql.saveTurtle(turtle)
    for container in self.containers.itervalues():
      self.sql.saveContainer(container)
    self.pathing.save()
        
  def addBuilding(self, building): #x, y, z, building_name, mk=1):
    self.sql.saveBuilding(building)
    self.buildings[building.id] = building
    #self.buildings[(building_name,mk)] = {"type":building_name,"mk":mk,"x":x,"y":y,"z":z}
    
  #def delBuilding(self, 
        
  def addVariable(self, variable, save=False):
    assert isinstance(variable, Variable)
    
    self.variables[variable.name] = variable
    
  
  def addPlot(self, plot):
    self.sql.savePlot(plot)
    self.plots[plot.id] = plot
    self.__updateplotcache()
    
  def delPlot(self, x, z, wx=1, wz=1):
    for ox in range(0,wx):
      for oz in range(0,wz):
        del self.plots[(x+ox,z+oz)]
    self.__updateplotcache()
    
  def getPlots(self):
    return self.plots
  
  def getSizedPlots(self):
    return self.sizedplotcache
    
  def addTurtle(self, turtle):
    self.sql.saveTurtle(turtle)
    print("Added turtle {} => {}".format(turtle.id, turtle))
    self.turtles[turtle.id] = turtle
    print("Stored turtle {}".format(self.turtles[turtle.id]))
    print(self)
    
  def delTurtle(self, turtle):
    del self.turtles[turtle.id]
    self.sql.delTurtle(turtle.id)
    
  def claimTurtle(self, turtle):
    print("SYS: Claiming turtle")
    self.claims[turtle] = True
    
  def unclaimTurtle(self, turtle):
    print("SYS: Unclaiming turtle")
    del self.claims[turtle]
    
  def isClaimed(self, turtle):
    return turtle in self.claims
    
  def getTurtles(self):
    print("SYS: Getting turtles")
    print(self.turtles)
    print(self)
    return self.turtles.itervalues()
  
  def addContainer(self, container):
    self.sql.saveContainer(container)
    self.containers[container.id] = container
    
  def delContainer(self, container):
    del self.containers[container.id]
    self.sql.delContainer(container)
  
  def getContainers(self):
    print("SYSL Getting containers")
    return self.containers.itervalues()
  
  # Utility functions from old System
  def hasTurtle(self, name):
    return self.getTurtle(name) != None
  
  def getTurtle(self, name):
    for turtle in self.turtles.itervalues():
      if turtle.name == name:
        return turtle
    return None
  
  def findContainer(self, x, y, z):
    for container in self.containers.itervalues():
      if container.x == x and container.y == y and container.z == z:
        return container
    return None

"""
Variables are... weird.  They are dynamic and inspect the state of the system.
Like, the system knows exactly how many blocks of dirt are collected in storage blocks.
But it also knows how many of those blocks are in use, and thus how many are available.
"""

class Variable:
  def __init__(self, name, datatype):
    self.name = name
    self.value = None
    self.datatype = datatype
    
  def __eq__(self, other):
    return self.name == other.name
    
  def set(self, value):
    self.value = value
    
  def get(self):
    return self.value
  
  def canCompareTo(self, other):
    raise NotImplementedError()
  
  def doComparison(self, comp, other):
    # Pray this works
    if not self.canCompareTo(other):
      raise TypeError()
    
    if comp == "==":
      return self.get() == other.get()
    elif comp == ">":
      return self.get() > other.get()
    elif comp == "<":
      return self.get() < other.get()
    elif comp == "!=":
      return self.get() != other.get()
    elif comp == ">=":
      return self.get() >= other.get()
    elif comp == "<=":
      return self.get() <= other.get()
    else:
      raise LookupError()
  
class NumericVariable(Variable):
  def __init__(self, name, value=None):
    Variable.__init__(self, name, int)
    self.value = value
  
  def canCompareTo(self, other):
    return other.datatype in [int, float]
  
class BooleanVariable(Variable):
  def __init__(self, name, value=None):
    Variable.__init__(self, name, bool)
    self.value = value
  
  def canCompareTo(self, other):
    return other.datatype in [int, bool]
  
  def doComparison(self, comp, other):
    if other.datatype == int:
      return other.value != 0 if self.value else other.value == 0
    else:
      return Variable.doComparison(comp, other)
        
class TurtlesVariable(NumericVariable):
  def __init__(self, sys, type, is_free):
    NumericVariable.__init__(self, "turtles.{}{}".format(designationToStr(type), ".free" if is_free else ""))
    self.sys = sys
    self.type = type
    self.is_free = is_free
  
  def get(self):
    turtles = self.sys.getTurtles()
    count = 0
    for turtle in turtles:
      if (turtle.getDesignation() & self.type) == self.type:
        if self.is_free and self.sys.isClaimed(turtle):
          continue
        else:
          count += 1
    return count
  
class PlotsVariable(NumericVariable):
  def __init__(self, sys, wx, wz):
    assert isinstance(wx, int)
    assert isinstance(wz, int)
    assert isinstance(sys, System)
    NumericVariable.__init__(self, "plots.{}.{}".format(wx, wz))
    self.size = (wx, wz)
    self.sys = sys
    
  def get(self):
    if self.size in self.sys.getSizedPlots():
      return len(self.sys.getSizedPlots()[self.size])
    else:
      return 0

class BuildingsVariable(NumericVariable):
  def __init__(self, sys, building_type, mk, is_free):
    #assert isinstance(wx, int)
    #assert isinstance(wz, int)
    assert isinstance(sys, System)
    #NumericVariable.__init__(self, "plots.{}.{}".format(wx, wz))
    #self.size = (wx, wz)
    self.building_type = building_type
    self.mk = mk
    self.sys = sys
    
  def get(self):
    #if self.size in self.sys.getSizedPlots():
      #return len(self.sys.getSizedPlots()[self.size])
    #else:
    if self.is_free:
      return 0
    else:
      count = 0
      for building in sys.buildings.itervalues():
        if building.building_type == self.building_type and building.mk == self.mk:
          count += 1
      return count

class GoalComponent:
  def __init__(self):
    self.goal = None
    self.system = None
    
  def setParentGoal(self, goal):
    assert isinstance(goal, Goal)
    self.goal = goal
    
  def getParentGoal(self):
    return self.goal
  
  def setSystem(self, system):
    assert isinstance(system, System)
    self.system = system
  
class Goal:
  def __init__(self, name="", requirements=[], actions=[], results=[]):
    self.requirements = list(requirements)
    self.results = list(results)
    self.actions = list(actions)
    self.name = str(name)
    self.resolved = False
    self.completed = False
    self.goals = []
    self.variables = dict()
    self.turtletoaction = dict()
    self.resolving = False
    self.system = None
    
    for pair in [(self.results, Result), (self.actions, Action), (self.requirements, Requirement)]:
      for instance in pair[0]:
        assert isinstance(instance, pair[1])
    
  def __str__(self):
    return self.name
  
  def __getitem__(self, key):
    if key not in self.variables:
      raise IndexError(key)
    else:
      return self.variables[key]
  
  def __setitem__(self, key, value):
    self.variables[key] = value
    
  def __contains__(self, key):
    return key in self.variables
    
  def __deepcopy__(self, memo):
    assert self.system is not None
    
    name = copy.deepcopy(self.name, memo)
    requirements = copy.deepcopy(self.requirements, memo)
    actions = copy.deepcopy(self.actions, memo)
    results = copy.deepcopy(self.results, memo)
    newGoal = Goal(name, requirements, actions, results)
    
    for array in [requirements, actions, results]:
      for obj in array:
        obj.setParentGoal(newGoal)
        obj.setSystem(self.system)
    
    return newGoal
  
  def setSystem(self, system):
    assert isinstance(system, System)
    
    self.system = system
    
  def getPrereqs(self):
    return self.requirements
  
  def getPostreqs(self):
    return self.results
  
  def canResolve(self):
    if self.resolved:
      return True
    
    for goal in self.goals:
      if not goal.isResolved():
        return False
    return True
  
  def canStartResolving(self):
    for req in self.requirements:
      if not req.canClaim():
        return False
    return True
  
  def isResolved(self):
    return self.resolved
  
  def isResolving(self):
    return self.resolving
  
  def setResolved(self, b=True):
    for child in self.goals:
      child.setResolved()
    self.resolved = b
    
  def startResolving(self):
    assert self.canStartResolving()
    for req in self.requirements:
      if not req.claim():
        print("Requirement '<{}>{}' went insane, invalidating goal".format(req.__class__.__name__,req))
        self.completed = True
        raise RuntimeError("Insane Requirement")
    self.resolving = True
  
  def getActions(self):
    return self.actions
  
  def getChildGoals(self):
    return self.goals
  
  def addChildGoal(self, goal):
    assert isinstance(goal, Goal)

    self.goals.append(goal)
    
  def clearChildGoals(self):
    self.goals = []
    
  def isCompleted(self):
    return self.completed
    
  def getResponse(self, turtle):
    assert isinstance(turtle, Turtle)
    
    for req in self.requirements:
      if not req.isClaimed():
        print(str(req) + " is not claimed, can't generate response")
        return False
    # Get the next action to perform and send its command
    for action in self.actions:
      if not action.isInvoked() and not action.isCompleted():
        self.turtletoaction[turtle] = action
        print(action)
        self.resolving = True
        return action.invoke(turtle)
    self.completed = True
    print("Goal finished!!!")
    return None
  
  def handleReply(self, turtle, reply):
    print("Got a reply!")
    if turtle not in self.turtletoaction:
      raise LookupError("Turtle not invoking anything")
    else:
      action = self.turtletoaction[turtle]
      return action.handleResponse(turtle, reply)
        
  def __str__(self):
    return self.name
  
  def __hash__(self):
    return id(self)
  
class BasicGoal(Goal):
  def __init__(self, name, requirements, actions, results):
    Goal.__init__(self, name, requirements, actions, results)
    
  def __str__(self):
    return self.name
    
class Requirement(GoalComponent):
  def __init__(self, name=""):
    GoalComponent.__init__(self)
    self.name = name
    self.claimed = False
    
  def __str__(self):
    return self.name
    
  def canClaim(self):
    raise NotImplementedError()
  
  def claim(self):
    raise NotImplementedError()
  
  def isClaimed(self):
    return self.claimed
    
class VariableRequirement(Requirement):
  def __init__(self, name, variable, comparison, value):
    Requirement.__init__(self, name=name)
    assert isinstance(variable, str), "variable must be str"
    self.variable = variable
    self.comparison = comparison
    self.value = value
    
  def canClaim(self):
    print(self.name)
    print(self.variable)
    if isinstance(self.variable, Variable):
      var = self.variable
    elif self.variable in self.system.variables:
      var = self.system.variables[self.variable]
    else:
      return False
    return var.doComparison(self.comparison, self.value)
    
  def claim(self):
    if self.variable in self.system.variables:
      var = self.system.variables[self.variable]
      var.set(var.get() - self.value.get())
      self.claimed = True
      return True
    else:
      return False
    
class PlotRequirement(Requirement):
  def __init__(self, name, size):
    Requirement.__init__(self, name=name)
    self.size = size
    self.variable = "plots.{0}.{0}".format(size)
    
  def canClaim(self):
    return (self.size/16,self.size/16) in self.system.getSizedPlots()
  
  def claim(self):
    if self.canClaim():
      self.goal["pos"] = [0,0,0]
      self.claimed = True
      return False
    else:
      return False
    
class TurtleClaimRequirement(VariableRequirement):
  def __init__(self, name, designation):
    self.designation = designation
    self.variable = {Turtle.MINER:"turtles.miner.free", Turtle.BUILDER:"turtles.builder.free",Turtle.CRAFTER:"turtles.crafter.free"}[designation]
    VariableRequirement.__init__(self, name, self.variable, ">", NumericVariable("",0))
    self.turtle = None
  
  def getTurtle(self):
    return self.turtle
  
  def canClaim(self):
    print("Looking to claim a " + designationToStr(self.designation) + " turtle")
    turtles = self.system.getTurtles()
    for turtle in turtles:
      print("  Looking at {}".format(str(turtle)))
      if not self.system.isClaimed(turtle):
        print("  Not claimed")
        if (turtle.getDesignation() & self.designation) == self.designation:
          return True
        else:
          print("  Wrong designation, has {}, want {}".format(int(turtle.getDesignation()), int(self.designation)))
    return False
    
  def claim(self):
    turtles = self.system.getTurtles()
    print(turtles)
    for turtle in turtles:
      print(turtle)
      print(self.designation)
      if not self.system.isClaimed(turtle):
        if (turtle.getDesignation() & self.designation) == self.designation:
          # Claim
          self.system.claimTurtle(turtle)
          self.turtle = turtle
          turtle.setGoal(self.goal)
          self.claimed = True
          
          #key = ("turtle." + designationToStr(self.designation))
          key = "turtle"
          if key not in self.goal:
            self.goal[key] = []
          self.goal[key].append(turtle)
          return True
    return False
    
class Action(GoalComponent):
  def __init__(self, name=""):
    GoalComponent.__init__(self)
    self.name = name
    self.completed = False
    self.invoked = False
    
  def isCompleted(self):
    return self.completed
  
  def isInvoked(self):
    return self.invoked
  
  def invoke(self, turtle):
    raise NotImplementedError()
  
  def handleResponse(self, turtle, response):
    raise NotImplementedError()
  
class MoveAction(Action):
  def __init__(self, name):
    Action.__init__(self, name)
    self.turtle = None
    
  def validate(self, turtle):
    if "turtle" not in self.goal:
      raise RuntimeError("No turtle found that I can move")
    if "pos" not in self.goal:
      raise RuntimeError("No destination found for moving")
    if turtle != self.goal["turtle"][0]:
      return False
    return True
  
  def invoke(self, turtle):
    #for req in self.goal.getPrereqs():
      #if isinstance(req, TurtleClaimRequirement):
        #print("Found a turtle that I can move!")
        #return
    if not self.validate(turtle):
      return False
    else:
      self.invoked = True
      #return {"turtle":self.goal["turtle"][0],"destination":self.goal["pos"]}
      return genRPCCall("move", {"destination": self.goal["pos"]})
  
  def handleResponse(self, turtle, response):
    if not self.validate(turtle):
      return False
    else:
      if response["type"] == "success":
        self.completed = True
        return {}
      else:
        self.invoked = False
        self.completed = False
        return {"retry":True}
  
class FlattenAction(Action):
  def __init__(self, name, up=0, down=0, size=8):
    Action.__init__(self, name)
    self.up = up
    self.down = down
    self.size = size
    
  def validate(self, turtle):
    if "turtle" not in self.goal:
      raise RuntimeError("No turtle found")
    if turtle != self.goal["turtle"][0]:
      return False
    return True
  
  def invoke(self, turtle):
    if not self.validate(turtle):
      return False
    else:
      if "flatten.up" in self.goal:
        self.up = int(self.goal["flatten.up"])
      if "flatten.down" in self.goal:
        self.down = int(self.goal["flatten.down"])
      if "flatten.size" in self.goal:
        self.size = int(self.goal["flatten.size"])
      self.invoked = True
      return genRPCCall("flatten", {"up":self.up, "down":self.down, "size":self.size})
  
  def handleResponse(self, turtle, response):
    if not self.validate(turtle):
      return False
    else:
      if response["type"] == "success":
        self.completed = True
        return {}
      else:
        self.invoked = False
        self.completed = False
        return {"retry":True}
      
class MineAction(Action):
  def __init__(self, name, block_name, count):
    Action.__init__(self, name)
    self.block_name = block_name
    self.count = count
    self.params = {}
    
  def validate(self, turtle):
    if "turtle" not in self.goal:
      raise RuntimeError("No turtle found")
    #elif "block" not in self.goal or "item" not in self.goal:
      #raise RuntimeError("No block or item found")
    elif turtle != self.goal["turtle"][0]:
      return False
    else:
      #if "block" in self.goal:
        #self.params["block"] = self.goal["block"]
      #else:
        #self.params["item"] = self.goal["item"]
      self.params["block"] = self.block_name
      self.params["count"] = self.count
      return True
    
  def invoke(self, turtle):
    if not self.validate(turtle):
      return False
    else:
      return genRPCCall("mine", self.params)
    
class ExploreAction(Action):
  def __init__(self, name, distance):
    Action.__init__(self, name)
    self.distance = distance
    self.params = {"distance":distance}
    
  def validate(self, turtle):
    if "turtle" not in self.goal:
      raise RuntimeError("No turtle found")
    elif turtle != self.goal["turtle"][0]:
      return False
    else:
      return True
    
  def invoke(self, turtle):
    if not self.validate(turtle):
      return False
    else:
      return genRPCCall("explore", self.params)
    
  def handleResponse(self, turtle, response):
    if not self.validate(turtle):
      return False
    elif response["type"] == "success":
      self.completed = True
      return {}
    else:
      self.invoked = False
      self.completed = False
      return {"retry":False}
    
    
class DiscoverAction(Action):
  def __init__(self, name):
    Action.__init__(self, name)
    
  def validate(self, turtle):
    if "turtle" not in self.goal:
      raise RuntimeError("No turtle found")
    elif turtle != self.goal["turtle"][0]:
      return False
    else:
      return True
    
  def invoke(self, turtle):
    if not self.validate(turtle):
      return False
    else:
      return genRPCCall("discover", {})
    
  def handleResponse(self, turtle, response):
    if not self.validate(turtle):
      return False
    elif response["type"] == "success":
      self.completed = True
      return {}
    else:
      self.invoked = False
      self.completed = False
      return {"retry":False}

class Result(GoalComponent):
  def __init__(self, name=""):
    GoalComponent.__init__(self)
    self.name = name
    
  def __str__(self):
    return self.name
  
  def getHelpfulness(self, goal):
    raise NotImplementedError()
      
class VariableIncreaseAction(Result):
  def __init__(self, name, variable, amount):
    Result.__init__(self, name=name)
    assert isinstance(variable, str), "variable must be str"
    self.variable = variable
    self.amount = amount
  
  def getHelpfulness(self, req):
    if isinstance(req, VariableRequirement):
      print("{} -- {}".format(req.variable, self.variable))
      if req.variable == self.variable:
        print(1)
        if req.comparison in ["=", ">", ">="]:
          print(2)
          return self.amount
        elif req.comparison in ["<", "<="]:
          print(3)
          return -self.amount
    elif isinstance(req, VariableDecreaseAction):
      if req.variable == self.variable:
        return -req.amount
    return 0
      
class VariableDecreaseAction(Result):
  def __init__(self, name, variable, amount):
    Result.__init__(self, name=name)
    assert isinstance(variable, str), "variable must be str"
    self.variable = variable
    self.amount = amount
  
  def getHelpfulness(self, req):
    if isinstance(req, VariableRequirement):
      if req.variable == self.variable:
        if req.comparison in ["=", "<", "<="]:
          return self.amount
        elif req.comparison in [">", ">="]:
          return -self.amount
    elif isinstance(req, VariableIncreaseAction):
      if req.variable == self.variable:
        return -req.amount
    return 0
  
sys = System("goap.db")
needsMiner = TurtleClaimRequirement("need miner", Turtle.MINER)
needsBuilder = TurtleClaimRequirement("need builder", Turtle.BUILDER,)
needsHouseResources = VariableRequirement("need house resources", "resources.dirt", ">=", NumericVariable("",5))
needsMine = VariableRequirement("need mine", "buildings.mine", ">=", NumericVariable("",1))
needs16Plot = PlotRequirement("need 16x16 plot", 16)
getsDirt = VariableIncreaseAction("get dirt", "resources.dirt", 1)
gets5Dirt = VariableIncreaseAction("get 5 dirt", "resources.dirt", 5)
getsHouse = VariableIncreaseAction("get house", "buildings.house", 1)
getsMine = VariableIncreaseAction("get mine", "buildings.mine", 1)
losesHouse = VariableDecreaseAction("lose house", "buildings.house", 1)
needsHouse = VariableRequirement("need house", "buildings.house", "==", 1)
buildMine = BasicGoal("build mine", [needsBuilder, needs16Plot], [MoveAction("move turtle to mine"), FlattenAction("flatten mine surface")], [getsMine])
gatherDirt = BasicGoal("gather dirt", [needsMiner, needsMine], [], [getsDirt])
deconHouse = BasicGoal("decon house", [needsMiner, needsHouse], [], [gets5Dirt, losesHouse])
buildHouse = BasicGoal("build house", [needsBuilder, needsHouseResources], [], [getsHouse])

for b in [True, False]:
  for d in [Turtle.BUILDER, Turtle.CRAFTER, Turtle.FARMER, Turtle.FORRESTER, Turtle.MINER]:
    sys.addVariable(TurtlesVariable(sys, d, b))
sys.variables["buildings.house"] = NumericVariable("buildings.house",0)
sys.variables["buildings.mine"] = NumericVariable("buildings.mine",0)
sys.variables["resources.dirt"] = NumericVariable("resources.dirt",0)
#sys.variables["plots.16.16"] = NumericVariable("",1)

class GoalLoader:
  COMPARISONS = ["==","!=","<",">",">=","<="]
  ASSIGNMENTS = ["+=", "-="]
  
  def __init__(self, resolver):
    assert isinstance(resolver, GoalResolver)
    
    self.resolver = resolver
    
  def __parsepart(self, string):
    if string in self.resolver.system.variables:
      return self.resolver.system.variables[string]
    else:
      return self.__loadvariable(string)
    
  def __loadvariable(self, varstr):
    assert isinstance(varstr, str)
    
    try:
      return NumericVariable("", int(varstr))
    except ValueError:
      pass
    try:
      return NumericVariable("", float(varstr))
    except ValueError:
      pass
    if re.match("true|1|yes|on", varstr, re.IGNORECASE):
      return BooleanVariable("",True)
    elif re.match("false|0|no|off", varstr, re.IGNORECASE):
      return BooleanVariable("",False)
    m = re.match("plot\(([^\)]+)\)", varstr, re.IGNORECASE)
    if m:
      parts = m.groups()[0].split(",")
      if len(parts) == 1:
        parts.append(parts[0])
      return self.resolver.system.variables["plots.{0}.{0}".format(parts[0], parts[1])]
    m = re.match("turtle\((miner|builder|crafter|forrester|farmer)\)", varstr, re.IGNORECASE)
    if m:
      return self.resolver.system.variables["turtles.{}.free".format(m.groups()[0])]
    # Whelp
    return varstr
  
  def __loadrequirement(self, req):
    assert "name" in req, "requirement needs 'name'"
    assert "needs" in req, "requirement needs 'needs'"
    assert isinstance(req["name"], str), "name must be string"
    assert isinstance(req["needs"], str) or isinstance(req["needs"], list), "needs must be string or list of strings"
    
    # FIXME: Splitting like this is bad, depends on single spaces
    if isinstance(req["needs"], str):
      needs = [req["needs"]]
    else:
      needs = req["needs"]
      
    for need in needs:
      assert isinstance(need, str), "needs must be string or list of strings"
      
      parts = [self.__parsepart(x) for x in need.split(" ")]
      
      if len(parts) == 3:
        # Assume variable comparison
        if parts[1] in self.COMPARISONS and (isinstance(parts[0], Variable) and isinstance(parts[2], Variable)):
          print("Variable comparison")
          #return VariableRequirement(req["name"], parts[0] if isinstance(parts[0], Variable) else parts[2], parts[1], self.__loadvariable(parts[2] if isinstance(parts[0], Variable) else parts[0]))
          assert parts[0].name != "", "lvalue must be non-local variable/value"
          
          if isinstance(parts[0], TurtlesVariable):
            return TurtleClaimRequirement(req["name"], parts[0].type)
          else:
            return VariableRequirement(req["name"], parts[0].name, parts[1], parts[2])
        else:
          print(parts[1] in self.COMPARISONS)
          print("Unk1")
      elif len(parts) == 1:
        #v = self.__loadvariable(parts[0])
        #if v:
        assert isinstance(parts[0], Variable), "lvalue is not local or global variable: {} {}".format(parts[0], type(parts[0]))
        assert parts[0].name != "", "lvalue must be non-local variable/value"
        
        if isinstance(parts[0], TurtlesVariable):
          return TurtleClaimRequirement(req["name"], parts[0].type)
        else:
          return VariableRequirement(req["name"], parts[0].name, ">", NumericVariable("Z",0))
        #else:
          #print("Unk3")
      else:
        print("Unk2")
    
  def __loadresult(self, result):
    assert "name" in result, "result needs 'name'"
    assert "gets" in result, "result needs 'gets'"
    assert isinstance(result["name"], str), "name must be string"
    assert isinstance(result["gets"], str) or isinstance(result["gets"], list), "gets must be string or list of strings"
    
    if isinstance(result["gets"], str):
      gets = [result["gets"]]
    else:
      gets = result["gets"]
      
    for get in gets:
      assert isinstance(get, str), "gets must be string or list of strings"
      
      parts = [self.__parsepart(x) for x in get.split(" ")]
      
      if len(parts) == 3:
        if parts[1] in self.ASSIGNMENTS and (isinstance(parts[0], Variable) and isinstance(parts[2], Variable)):
          print("Variable modification")
          assert parts[0].name != "", "lvalue must be non-local variable/value"
          if parts[1] == "+=":
            return VariableIncreaseAction(result["name"], parts[0].name, parts[2])
          elif parts[1] == "-=":
            return VariableDecreaseAction(result["name"], parts[0].name, parts[2])
        else:
          print("Unk")
      elif len(parts) == 1:
        assert parts[0].name != "", "lvalue must be non-local variable/value"
        return VariableIncreaseAction(result["name"], parts[0].name, NumericVariable("",1))
      else:
        print("Unk")
        
  def __loadaction(self, action):
    assert "name" in action, "action needs 'name'"
    assert "does" in action, "action needs 'does'"
    assert isinstance(action["name"], str), "name must be string"
    assert isinstance(action["does"], str), "does must be string"
    
    does = action["does"]
    name = action["name"]
    
    if re.match("move", does, re.IGNORECASE):
      return MoveAction(name)
    elif re.match("flatten", does, re.IGNORECASE):
      return FlattenAction(name, 1)
    elif re.match("mine", does, re.IGNORECASE):
      assert "vars" in action, "action needs vars"
      assert "block" in action["vars"], "needs block name"
      assert "count" in action["vars"], "needs block count"
      return MineAction(name, block_name=action["vars"]["block"], count=int(action["vars"]["count"]))
    elif re.match("explore", does, re.IGNORECASE):
      assert "vars" in action, "action needs vars"
      assert "distance" in action["vars"], "needs distance"
      return ExploreAction(name, distance=int(action["vars"]["distance"]))
    elif re.match("discover", does, re.IGNORECASE):
      return DiscoverAction(name)
    else:
      print("Unk")
      
  def __loadgoal(self, goal, l_reqs, l_actions, l_results):
    assert "name" in goal, "goal needs 'name'"
    assert isinstance(goal["name"], str), "name must be string"
    
    reqs = goal["needs"] if "needs" in goal else []
    actions = goal["does"] if "does" in goal else []
    results = goal["gets"] if "gets" in goal else []
    
    if isinstance(reqs, str):
      reqs = [reqs]
    if isinstance(actions, str):
      actions = [actions]
    if isinstance(results, str):
      results = [results]
    
    i_reqs = []
    i_actions = []
    i_results = []
    
    for req in reqs:
      if req not in l_reqs:
        raise KeyError("requirement '{}' does not exist".format(req))
      else:
        i_reqs.append(l_reqs[req])
    for action in actions:
      if action not in l_actions:
        raise KeyError("action '{}' does not exist".format(action))
      else:
        i_actions.append(l_actions[action])
    for result in results:
      if result not in l_results:
        raise KeyError("result '{}' does not exist".format(result))
      else:
        i_results.append(l_results[result])
        
    return BasicGoal(goal["name"], i_reqs, i_actions, i_results)
    
  def load(self, filename):
    reqs = {}
    results = {}
    actions = {}
    goals = {}
    with open(filename, 'r') as f:
      objs = load_all(f, Loader=Loader)
      f_reqs = []
      f_results = []
      f_actions = []
      f_goals = []
      
      for obj in objs:
        print(obj)
        if "requirement" in obj:
          f_reqs.append(obj["requirement"])
        elif "result" in obj:
          f_results.append(obj["result"])
        elif "action" in obj:
          f_actions.append(obj["action"])
        elif "goal" in obj:
          f_goals.append(obj["goal"])
          
      for result in f_results:
        print(result)
        r=self.__loadresult(result)
        if r:
          results[r.name] = r
        else:
          print("Invalid result")
      for req in f_reqs:
        r=self.__loadrequirement(req)
        if r:
          reqs[r.name] = r
        else:
          print("Invalid requirement")
      for action in f_actions:
        a=self.__loadaction(action)
        if a:
          actions[a.name] = a
        else:
          print("Invalid action")
      for goal in f_goals:
        g=self.__loadgoal(goal, reqs, actions, results)
        if g:
          goals[g.name] = g
          self.resolver.addGoal(g)
        else:
          print("Invalid goal")
"""
Actions need to know certain things before running. Reqs and other actions should set variables in the goal
that all other actions can use.

Things like building something, it needs a turtle. Req. will claim one and make it available to the goal.
Next, a location to build needs to be determined. So, a req to find a building place will set the location.

These are all GENERIC!  Actions can be mixed and matched and still use common variables to get the job done.
That said, for a requirement to find a storage containing X, you can then use the build action to build at that position.
tl;dr, goals must be very specific and limited in what they do.
"""

"""
goals = [gatherDirt, buildHouse, deconHouse, buildMine]
currentgoals = []

def addGoal(goal):
  currentgoals.append(copy.deepcopy(goal))

def isCounterProductive(prereqs, postreqs):
  for req in prereqs:
    for action in postreqs:
      if action.getHelpfulness(req) < 0:
        return True
  return False

def resolveGoal(g):
  all = True
  score = 0
  reqActions = dict()
  print("Trying to " + str(g))
  for req in g.getPrereqs():
    print("looking at requirement for " + req.name)
    if req.canClaim():
      print("  Can already claim it")
      reqActions[req] = None
    else:
      reqActions[req] = []
      for goal2 in goals:
        for action in goal2.getPostreqs():
          s = action.getHelpfulness(req)
          if s > 0:
            print("  action " + action.name + " from " + goal2.name + " has a helpfulness of " + str(s))
            if isCounterProductive(g.getPostreqs(), goal2.getPostreqs()):
              print("    but action " + action.name + " is counter-productive!")
            else:
              reqActions[req].append((s, action, goal2))
      reqActions[req] = sorted(reqActions[req], key = lambda x: x[0], reverse=True)
  
  # We can pick goals from our actions list. Find each variation and sort by difficulty
  neededGoals = []
  for reqs in reqActions.itervalues():
    if reqs != None and len(reqs) > 0:
      neededGoal = reqs[0]
      print("I need " + str(neededGoal[2]) + " to " + str(neededGoal[1]) + " (helpfulness " + str(neededGoal[0]) + ")")
      neededGoals.append(neededGoal[2])
      goal = copy.deepcopy(neededGoal[2])
      g.addChildGoal(goal)
      resolveGoal(goal)
  return neededGoals

addGoal(buildHouse)
resolveGoal(currentgoals[0])

leaf = copy.deepcopy(currentgoals[0].getChildGoals()[0].getChildGoals()[0])
# You don't need to mark that you are working on this goal because there should only be one
# scope with this goal in it.
print("------")
for req in leaf.getPrereqs():
  print(req)
  print("  Can claim: " + str(req.canClaim()))
  if not req.canClaim():
    print("  Goal is invalid, rethink")
    break
  print("  "+str(req.claim()))
  if req.name == "need builder":
    print("  "+str(req.turtle))
    print("  "+str(req.claimed))
    turtle = req.turtle
  else:
    print("  Not a builder")
# Now, to get things done, get a leaf goal, make sure it is claimable, claim it if not already, get an action not finished and perform it.

print("Response:")
print(turtle.getResponse())
print(turtle.handleResponse({"type":"success"}))
print("Response:")
print(turtle.getResponse())
print(turtle.handleResponse({"type":"success"}))
print("Response:")
print(turtle.getResponse())

print("At this point, this goal is all out of things to do")

"""

# Prototype for the resolver class
class GoalResolver:
  def __init__(self):
    self.currentGoals = []
    self.allGoals = []
    self.resolvingGoals = []
    self.system = sys
    self.rpcIdToGoal = {}

  def __isCounterProductive(self, prereqs, postreqs):
    for req in prereqs:
      for action in postreqs:
        if action.getHelpfulness(req) < 0:
          return True
    return False
  
  def doGoal(self, goal, name=None):
    clone = copy.deepcopy(goal)
    
    if name:
      clone.name = name
      
    self.currentGoals.append(clone)
    self.resolveGoals()
  
  def addGoal(self, goal):
    assert isinstance(goal, Goal)
    self.allGoals.append(goal)
    goal.setSystem(self.system)
    
  def stopGoal(self, goal):
    assert goal in self.currentGoals
    
    del self.currentGoals[goal]
  
  def __resolve(self, goal):
    all = True
    score = 0
    reqActions = dict()
    print("Trying to " + str(goal))
    for req in goal.getPrereqs():
      print("looking at requirement for " + req.name)
      print(isinstance(req, TurtleClaimRequirement))
      if req.canClaim():
        print("  Can already claim it")
        reqActions[req] = None
      else:
        reqActions[req] = []
        for goal2 in self.allGoals:
          for action in goal2.getPostreqs():
            s = action.getHelpfulness(req)
            print("{} has {} helpfulness".format(action, s))
            if isinstance(s, NumericVariable):
              s=s.value
            if s > 0:
              print("  action " + action.name + " from " + goal2.name + " has a helpfulness of " + str(s))
              if self.__isCounterProductive(goal.getPostreqs(), goal2.getPostreqs()):
                print("    but action " + action.name + " is counter-productive!")
              else:
                reqActions[req].append((s, action, goal2))
        reqActions[req] = sorted(reqActions[req], key = lambda x: x[0], reverse=True)
    
    # We can pick goals from our actions list. Find each variation and sort by difficulty
    neededGoals = []
    goal.clearChildGoals()
    for reqs in reqActions.itervalues():
      if reqs != None and len(reqs) > 0:
        neededGoal = reqs[0]
        print("I need " + str(neededGoal[2]) + " to " + str(neededGoal[1]) + " (helpfulness " + str(neededGoal[0]) + ")")
        neededGoals.append(neededGoal[2])
        goalcopy = copy.deepcopy(neededGoal[2])
        goal.addChildGoal(goalcopy)
        if not self.__resolve(goalcopy):
          return False
      elif reqs != None and len(reqs) == 0:
        print("Some requirement couldn't be satisfied")
        return False
    return True
  
  def resolveGoals(self):
    # For all goals added, resolve any that are yet to be resolved
    # For all goals that are done, remove them from their parent.
    for goal in self.currentGoals:
      if not goal.isResolving():
        resolved = self.__resolve(goal)
        print("Resolving goal {} was {}".format(goal, resolved))
        if resolved:
          goal.setResolved(True)
  
  # Dict of goal to array of child goals
  def getGoals(self):
    def recGetGoals(goal):
      if len(goal.getChildGoals()) == 0:
        return {}
      else:
        ret = {}
        for child in goal.getChildGoals():
          ret[child] = recGetGoals(child)
        return ret
        
    ret = {}
    for goal in self.currentGoals:
      ret[goal] = recGetGoals(goal)
    return ret
  
  def getAllGoals(self):
    return list(self.allGoals)
  
  def __getLeafGoals(self, goal):
    assert isinstance(goal, Goal)
    if len(goal.getChildGoals()) > 0:
      rets = []
      for child in goal.getChildGoals():
        if child.isResolved() and not child.isCompleted() and not child.isResolving():
          rets.extend(self.__getLeafGoals(child))
        return rets
    else:
      return [goal]
    
  def getAction(self, turtle):
    for goal in self.resolvingGoals:
      print("Looking at goal currently resolving {}".format(goal))
      if "turtle" in goal.variables:
        print("Goal has turtle(s)")
      if "turtle" in goal.variables and turtle in goal.variables["turtle"]:
        print("Found goal '{}' which uses turtle '{}'".format(goal, turtle))
        rpc = goal.getResponse(turtle)
        if rpc and isinstance(rpc, dict):
          self.rpcIdToGoal[rpc["id"]] = goal
          return rpc
      
    newLeafs = False
    for goal in self.currentGoals:
      assert isinstance(goal, Goal)
      print("Looking for leaf goals in '{}'".format(goal))
      leafs = self.__getLeafGoals(goal)
      
      if len(leafs) > 0:
        for leaf in leafs:
          if leaf:
            print("  Found leaf goal '{}'".format(leaf))
            if leaf.canStartResolving():
              print("  It can start resolving")
              leaf.startResolving()
              self.resolvingGoals.append(leaf)
              newLeafs = True
    if newLeafs:
      print("Trying to get action again")
      return self.getAction(turtle)
    else:
      print("No new leafs")
      # TODO: Add in idle actions! Things to keep them busy, like mining or exploring.
      return None
    
  def handleReply(self, turtle, response):
    assert isinstance(response, dict)
    assert "id" in response
    
    if response["id"] in self.rpcIdToGoal:
      print("I was expecting this response!")
      goal = self.rpcIdToGoal[response["id"]]
      del self.rpcIdToGoal[response["id"]]
      assert isinstance(goal, Goal)
      # TODO: handle the reply dict to see what should happen with the goal.
      # If retry is false, destroy the goal and re-resolve it.  Maybe try and hint
      # at what the problem is?  If trying to build and the plot suddenly isn't clear,
      # Maybe, redo the build?  Or maybe force a goal to be added?
      # A flatten goal would unclaim the current goal, decon what's built, then try
      # it again.
      return goal.handleReply(turtle, response)
        
  # More?
  # Maybe system shouldn't be passed in on creation of goals, actions, reqs, res.
  #   This class can add them when they get stored.
