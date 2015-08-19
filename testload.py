#!/usr/bin/env python

from ccturtle.goap.goap import GoalLoader, GoalResolver
from ccturtle.turtle import Turtle

g = GoalResolver()
s = g.system
l = GoalLoader(g)

t = Turtle("1", 0, 0, 0, 0)
t.setDesignation(Turtle.BUILDER)
s.addTurtle(t)

l.load("test.yml")

goals = {}
for goal in g.getAllGoals():
  print(str(goal))
  goals[goal.name] = goal
  
g.doGoal(goals["build mine"])
g.resolveGoals()

