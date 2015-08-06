#!/usr/bin/env python

import copy

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
    
  def __str__(self):
    return self.name
  
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
    
  def __str__(self):
    return self.name
    
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
    
  def __str__(self):
    return self.name
  
  def getHelpfulness(self, goal):
    raise NotImplementedError()
      
class VariableIncreaseAction(Action):
  def __init__(self, name, variable, amount):
    Action.__init__(self, name=name)
    self.variable = variable
    self.amount = amount
  
  def getHelpfulness(self, req):
    if isinstance(req, VariableRequirement):
      if req.variable == self.variable:
        if req.comparison in ["=", ">", ">="]:
          return self.amount
        elif req.comparison in ["<", "<="]:
          return -self.amount
    elif isinstance(req, VariableDecreaseAction):
      if req.variable == self.variable:
        return -req.amount
    return 0
      
class VariableDecreaseAction(Action):
  def __init__(self, name, variable, amount):
    Action.__init__(self, name=name)
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
  
needsMiner = VariableRequirement("need miner", "turtles.miner.free", ">=", NumericVariable("", 1))
needsBuilder = VariableRequirement("need miner", "turtles.builder.free", ">=", NumericVariable("", 1))
needsHouseResources = VariableRequirement("need house resources", "resources.dirt", ">=", NumericVariable("",5))
needsMine = VariableRequirement("need mine", "buildings.mine", ">=", NumericVariable("",1))
getsDirt = VariableIncreaseAction("get dirt", "resources.dirt", 1)
gets5Dirt = VariableIncreaseAction("get 5 dirt", "resources.dirt", 5)
getsHouse = VariableIncreaseAction("get house", "buildings.house", 1)
getsMine = VariableIncreaseAction("get mine", "buildings.mine", 1)
losesHouse = VariableDecreaseAction("lose house", "buildings.house", 1)
needsHouse = VariableRequirement("need house", "buildings.house", "==", 1)
buildMine = BasicGoal("build mine", [], [getsMine])
gatherDirt = BasicGoal("gather dirt", [needsMiner, needsMine], [getsDirt])
deconHouse = BasicGoal("decon house", [needsMiner, needsHouse], [gets5Dirt, losesHouse])
buildHouse = BasicGoal("build house", [needsBuilder, needsHouseResources], [getsHouse])

variables["turtles.miner.free"] = NumericVariable("",1)
variables["turtles.builder.free"] = NumericVariable("",1)
variables["buildings.house"] = NumericVariable("",0)
variables["resources.dirt"] = NumericVariable("",0)

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
      neededGoals.extend(resolveGoal(neededGoal[2]))
  return neededGoals

addGoal(buildHouse)
resolveGoal(currentgoals[0])