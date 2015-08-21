#!/usr/bin/env python

from ccturtle.goap.goap import GoalLoader, GoalResolver
from ccturtle.turtle import Turtle

g = GoalResolver()
s = g.system
l = GoalLoader(g)

for plot in s.getPlots():
  s.delPlot(plot)
for turtle in s.getTurtles():
  s.delTurtle(turtle)

t = Turtle("1", 0, 0, 0, 0)
t.setDesignation(Turtle.BUILDER)
s.addTurtle(t)

l.load("test.yml")

for key, val in s.variables.iteritems():
  print("{} => {}".format(str(key), str(val.value)))
  
goals = {}
for goal in g.getAllGoals():
  print(str(goal))
  goals[goal.name] = goal
  
g.doGoal(goals["build mine"])
g.resolveGoals()

print("------ Getting action")
print(g.getAction(t))