#!/usr/bin/env python

import copy
from ccturtle.turtle import Turtle

class System:
  def __init__(self):
    self.turtles = [Turtle("1", 0, 0, 0, 0), Turtle("2", 0, 0, 0, 0)]
    self.turtles[0].setDesignation(Turtle.MINER)
    self.turtles[1].setDesignation(Turtle.CRAFTER)
    self.claims = dict()
  
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
    return self.turtles
  
variables = dict()

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
#    super(Variable, self).__init__(name, int)
    self.value = value
  
  def canCompareTo(self, other):
    return other.datatype in [int, float]
  
class TurtlesMinersVariable(NumericVariable):
  def __init__(self, sys):
    NumericVariable.__init__(self, "turtles.miners")
    self.sys = sys
  
  def get(self):
    turtles = self.sys.getTurtles()
    count = 0
    for turtle in turtles:
      if turtle.getDesignation() == Turtle.MINER:
        count += 1
    return count
  
class TurtlesMinersFreeVariable(NumericVariable):
  def __init__(self, sys):
    NumericVariable.__init__(self, "turtles.miners.free")
    self.sys = sys
    
  def get(self):
    turtles = self.sys.getTurtles()
    count = 0
    for turtle in turtles:
      if turtle.getDesignation() == Turtle.MINER:
        if not self.sys.isClaimed(turtle):
          count += 1
    return count

class Goal:
  def __init__(self, name="", requirements=[], actions=[], results=[]):
    self.requirements = list(requirements)
    self.results = list(results)
    self.actions = list(actions)
    self.name = str(name)
    self.resolved = False
    self.goals = []
    
  def __str__(self):
    return self.name
  
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
      
    for pre in self.requirements:
      if not pre.isResolved():
        return False
    return True
  
  def isResolved(self):
    return self.resolved
  
  def getActions(self):
    return self.actions
  
  def getChildGoals(self):
    return self.goals
  
  def addChildGoal(self, goal):
    self.goals.append(goal)
    
  def __str__(self):
    return self.name
  
  def __eq__(self, other):
    raise NotImplementedError()
  
class BasicGoal(Goal):
  def __init__(self, name, requirements, actions, results):
    Goal.__init__(self, name, requirements, actions, results)
    
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
    
class TurtleClaimRequirement(VariableRequirement):
  def __init__(self, name, designation, sys):
    self.designation = designation
    self.variable = {Turtle.MINER:"turtles.miner.free", Turtle.BUILDER:"turtles.builder.free",Turtle.CRAFTER:"turtles.crafter.free"}[designation]
    VariableRequirement.__init__(self, name, self.variable, ">", NumericVariable("",0))
    self.sys = sys
    self.turtle = None
  
  def getTurtle(self):
    return self.turtle
  
  def claim(self):
    turtles = self.sys.getTurtles()
    for turtle in turtles:
      if turtle.getDesignation() == self.designation:
        # Claim
        self.sys.claimTurtle(turtle)
        self.turtle = turtle
    
class Action:
  def __init__(self, name="", goal=None):
    self.name = name
    self.completed = False
    self.goal = goal
    
  def isCompleted(self):
    return self.completed
  
  def invoke(self):
    raise NotImplementedError()
  
  def handleResponse(self):
    raise NotImplementedError()
  
class MoveAction(Action):
  def __init__(self, name, goal):
    Action.__init__(self, name, goal)
    self.turtle = None
    
  def invoke(self):
    for req in self.goal.getPrereqs():
      if isinstance(req, TurtleClaimRequirement):
        print("Found a turtle that I can move!")
        return
    raise RuntimeError("No turtle found that I can move")

class Result:
  def __init__(self, name=""):
    self.name = name
    
  def __str__(self):
    return self.name
  
  def getHelpfulness(self, goal):
    raise NotImplementedError()
      
class VariableIncreaseAction(Result):
  def __init__(self, name, variable, amount):
    Result.__init__(self, name=name)
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
      
class VariableDecreaseAction(Result):
  def __init__(self, name, variable, amount):
    Result.__init__(self, name=name)
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
  
sys = System()
needsMiner = TurtleClaimRequirement("need miner", Turtle.MINER, sys)
needsBuilder = TurtleClaimRequirement("need builder", Turtle.BUILDER, sys)
needsHouseResources = VariableRequirement("need house resources", "resources.dirt", ">=", NumericVariable("",5))
needsMine = VariableRequirement("need mine", "buildings.mine", ">=", NumericVariable("",1))
getsDirt = VariableIncreaseAction("get dirt", "resources.dirt", 1)
gets5Dirt = VariableIncreaseAction("get 5 dirt", "resources.dirt", 5)
getsHouse = VariableIncreaseAction("get house", "buildings.house", 1)
getsMine = VariableIncreaseAction("get mine", "buildings.mine", 1)
losesHouse = VariableDecreaseAction("lose house", "buildings.house", 1)
needsHouse = VariableRequirement("need house", "buildings.house", "==", 1)
buildMine = BasicGoal("build mine", [needsBuilder], [], [getsMine])
gatherDirt = BasicGoal("gather dirt", [needsMiner, needsMine], [], [getsDirt])
deconHouse = BasicGoal("decon house", [needsMiner, needsHouse], [], [gets5Dirt, losesHouse])
buildHouse = BasicGoal("build house", [needsBuilder, needsHouseResources], [], [getsHouse])

variables["turtles.miner.free"] = TurtlesMinersFreeVariable(sys)
variables["turtles.builder.free"] = TurtlesMinersVariable(sys)
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
      goal = copy.deepcopy(neededGoal[2])
      g.addChildGoal(goal)
      resolveGoal(goal)
  return neededGoals

addGoal(buildHouse)
resolveGoal(currentgoals[0])

# Now, to get things done, get a leaf goal, make sure it is claimable, claim it if not already, get an action not finished and perform it.
