#!/usr/bin/env python

import copy

"""
Variables are... weird.  They are dynamic and inspects the state of the system.
Like, the system knows exactly how many blocks of dirt are collected in storage blocks.
But it also knows how many of those blocks are in use, and thus how many are available.
"""

class Variable:
  def __init__(self, name, datatype):
    self.name = name
    self.value = None
    self.datatype = datatype
    
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
      return self.value == other.value
    elif comp == ">":
      return self.value > other.value
    elif comp == "<":
      return self.value < other.value
    elif comp == "!=":
      return self.value != other.value
    elif comp == ">=":
      return self.value >= other.value
    elif comp == "<=":
      return self.value <= other.value
    else:
      raise LookupError()
  
class NumericVariable(Variable):
  def __init__(self, name, value=None):
    Variable.__init__(self, name, int)
#    super(Variable, self).__init__(name, int)
    self.value = value
  
  def canCompareTo(self, other):
    return other.datatype in [int, float]
  
variables = dict()

class Goal:
  def __init__(self, name="", prereqs=[], postreqs=[]):
    self.prereqs = list(prereqs)
    self.postreqs = list(postreqs)
    self.name = str(name)
    self.resolved = False
  
  def getPrereqs(self):
    return self.prereqs
  
  def getPostreqs(self):
    return self.postreqs
  
  def canResolve(self):
    for pre in self.prereqs:
      if not pre.isResolved():
        return False
    return True
  
  def isResolved(self):
    return self.resolved
    
  def __str__(self):
    return self.name
  
  def __eq__(self, other):
    raise NotImplementedError()
  
class BasicGoal(Goal):
  def __init__(self, name, prereqs, postreqs):
    Goal.__init__(self, name=name, prereqs=prereqs, postreqs=postreqs)
    
class Requirement:
  def __init__(self, name=""):
    self.name = name
    
  def canClaim(self):
    raise NotImplementedError()
  
  def claim(self):
    raise NotImplementedError()
    
class VariableRequirement(Requirement):
  def __init__(self, name, variable, comparison, value):
    Requirement.__init__(self, name=name)
    self.variable = variable
    self.comparison = comparison
    self.value = value
    
  def canClaim(self):
    if variables.has_key(self.variable):
      var = variables[self.variable]
      
      return var.doComparison(self.comparison, self.value)
    else:
      return False

class Action:
  def __init__(self, name=""):
    self.name = name
    
  def getHelpfulness(self, goal):
    raise NotImplementedError()
      
class VariableIncreaseAction(Action):
  def __init__(self, name, variable, amount):
    Action.__init__(self, name=name)
    self.variable = variable
    self.amount = amount
  
  def getHelpfulness(self, req):
    if isinstance(req, VariableRequirement):
      if req.comparison in ["=", ">", ">="]:
        if req.variable == self.variable:
          return self.amount
    return 0
  
needsMiner = VariableRequirement("needs miner", "turtles.miner.free", ">=", NumericVariable("", 1))
needsBuilder = VariableRequirement("needs miner", "turtles.builder.free", ">=", NumericVariable("", 1))
needsHouseResources = VariableRequirement("needs house resources", "resources.dirt", ">=", NumericVariable("",5))
getsDirt = VariableIncreaseAction("gets dirt", "resources.dirt", 1)
getsHouse = VariableIncreaseAction("gets house", "buildings.house", 1)
gatherDirt = BasicGoal("gather dirt", [needsMiner], [getsDirt])
buildHouse = BasicGoal("build house", [needsBuilder, needsHouseResources], [getsHouse])
needsHouse = VariableRequirement("needs house", "buildings.house", "==", 1)

variables["turtles.miner.free"] = NumericVariable("",1)
variables["turtles.builder.free"] = NumericVariable("",1)
variables["buildings.house"] = NumericVariable("",0)
variables["resources.dirt"] = NumericVariable("",0)

goals = [gatherDirt, buildHouse]
currentgoals = []

def addGoal(goal):
  currentgoals.append(copy.deepcopy(goal))

def resolveGoal(g):
  all = True
  score = 0
  reqActions = dict()
  for req in g.getPrereqs():
    print("looking at req " + req.name)
    if req.canClaim():
      print("Can already claim it")
      reqActions[req] = None
    else:
      reqActions[req] = (0,None)
      for goal2 in goals:
        for action in goal2.getPostreqs():
          s = action.getHelpfulness(req)
          if s > 0:
            print("action " + action.name + " from " + goal2.name + " has a helpfulness of " + str(s))
            if s > reqActions[req][0]:
              reqActions[req] = (s, action)
  # We can pick goals from our actions list. Find each variation and sort by difficulty

addGoal(buildHouse)
resolveGoal(currentgoals[0])