#!/usr/bin/env python

import copy
from ccturtle.turtle import Turtle, designationToStr

# Temporary helper method, move to something more elegant in the future
rpc_call_id = 0
def genRPCCall(action_name, parameters):
  global rpc_call_id
  rpc_call_id += 1
  return {"action":action_name, "parameters":parameters, "id":rpc_call_id}

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
      if turtle.getDesignation() & Turtle.MINER:
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
      if turtle.getDesignation() & Turtle.MINER:
        if not self.sys.isClaimed(turtle):
          count += 1
    return count

class GoalComponent:
  def __init__(self):
    self.goal = None
    
  def setParentGoal(self, goal):
    self.goal = goal
    
  def getParentGoal(self):
    return self.goal
  
class Goal:
  def __init__(self, name="", requirements=[], actions=[], results=[]):
    self.requirements = list(requirements)
    self.results = list(results)
    self.actions = list(actions)
    self.name = str(name)
    self.resolved = False
    self.goals = []
    self.variables = dict()
    self.turtletoaction = dict()
    self.isResolving = True
    
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
    name = copy.deepcopy(self.name, memo)
    requirements = copy.deepcopy(self.requirements, memo)
    actions = copy.deepcopy(self.actions, memo)
    results = copy.deepcopy(self.results, memo)
    newGoal = Goal(name, requirements, actions, results)
    
    for array in [requirements, actions, results]:
      for obj in array:
        obj.setParentGoal(newGoal)
    
    return newGoal
  
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
  
  def isResolving(self):
    return self.isResolving
  
  def getActions(self):
    return self.actions
  
  def getChildGoals(self):
    return self.goals
  
  def addChildGoal(self, goal):
    self.goals.append(goal)
    
  def getResponse(self, turtle):
    for req in self.requirements:
      if not req.isClaimed():
        print(str(req) + " is not claimed, can't generate response")
        return False
    # Get the next action to perform and send its command
    for action in self.actions:
      if not action.isInvoked():
        self.turtletoaction[turtle] = action
        print(action)
        self.isResolving = True
        return action.invoke(turtle)
    self.resolved = True
    return "I guess this goal is done?"
  
  def handleReply(self, turtle, reply):
    print("Got a reply!")
    if turtle not in self.turtletoaction:
      raise LookupError("Turtle not invoking anything")
    else:
      action = self.turtletoaction[turtle]
      return action.handleResponse(turtle, reply)
        
  def __str__(self):
    return self.name
  
  def __eq__(self, other):
    raise NotImplementedError()
  
class BasicGoal(Goal):
  def __init__(self, name, requirements, actions, results):
    Goal.__init__(self, name, requirements, actions, results)
    
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
    self.variable = variable
    self.comparison = comparison
    self.value = value
    
  def canClaim(self):
    if variables.has_key(self.variable):
      var = variables[self.variable]

      return var.doComparison(self.comparison, self.value)
    else:
      return False
    
  def claim(self):
    if self.variable in variables:
      var = variables[self.variable]
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
    return True
  
  def claim(self):
    if self.canClaim():
      self.goal["pos"] = [0,0,0]
      self.claimed = True
      return False
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
      print(turtle.getDesignation())
      print(self.designation)
      if turtle.getDesignation() & self.designation:
        # Claim
        self.sys.claimTurtle(turtle)
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

variables["turtles.miner.free"] = TurtlesMinersFreeVariable(sys)
variables["turtles.builder.free"] = TurtlesMinersVariable(sys)
variables["buildings.house"] = NumericVariable("",0)
variables["resources.dirt"] = NumericVariable("",0)
variables["plots.16.16"] = NumericVariable("",1)

"""
Actions need to know certain things before running. Reqs and other actions should set variables in the goal
that all other actions can use.

Things like building something, it needs a turtle. Req. will claim one and make it available to the goal.
Next, a location to build needs to be determined. So, a req to find a building place will set the location.

These are all GENERIC!  Actions can be mixed and matched and still use common variables to get the job done.
That said, for a requirement to find a storage containing X, you can then use the build action to build at that position.
tl;dr, goals must be very specific and limited in what they do.
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

# Prototype for the resolver class
class GoalResolver:
  def __init__(self):
    self.currentGoals = []
    self.allGoals = []
    

  def __isCounterProductive(self, prereqs, postreqs):
    for req in prereqs:
      for action in postreqs:
        if action.getHelpfulness(req) < 0:
          return True
    return False
  
  def doGoal(self, goal):
    self.currentGoals.append(goal)
  
  def addGoal(self, goal):
    self.allGoals.append(goal)
  
  def __resolve(self, goal):
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
  
  def resolveGoals(self, system):
    for goal in self.currentGoals:
      if goal.
  
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
  
  # More?
