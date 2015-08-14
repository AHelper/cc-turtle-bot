#!/usr/bin/env python

from ccturtle.goap.goap import GoalLoader, GoalResolver

g = GoalResolver()
l = GoalLoader(g)

l.load("test.yml")

