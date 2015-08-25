#!/usr/bin/python

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

@package turtle
'''

import tornado
import tornado.escape
import tornado.ioloop
import tornado.web
import tornado.log
from tornado.web import HTTPError

from glob import glob
import os
import logging
from cStringIO import StringIO

from ccturtle import pathing
from ccturtle.requestparser import RequestValidator
from ccturtle.turtle import Turtle

from ccturtle.server import handlers
import ccturtle.server.json
#from ccturtle.system import System
from ccturtle.goap.goap import GoalResolver, GoalLoader

def createApp():
  #sys = System()
  resolver = GoalResolver()
  validator = RequestValidator()
  loader = GoalLoader(resolver)
          
  settings = {
    'default_handler_class': ccturtle.server.json.JSONErrorHandler,
    'default_handler_args': dict(status_code=404),
    'debug': True
  }
  
  init = {
    'sys': resolver.system,
    'resolver': resolver,
    'validator': validator
  }

  routes = [
    (r"/pathing/get", handlers.PathingGetHandler, init),
    (r"/pathing/set", handlers.PathingSetHandler, init),
    (r"/pathing/query", handlers.PathingQueryHandler, init),
    (r"/turtle/([^/]+)/register", handlers.RegisterTurtleHandler, init),
    (r"/turtle/([^/]+)/unregister", handlers.UnregisterTurtleHandler, init),
    (r"/turtle/([^/]+)/status", handlers.TurtleStatusHandler, init),
    (r"/turtle/([^/]+)/position", handlers.TurtlePositionHandler, init),
    (r"/turtle/([^/]+)/getAction", handlers.TurtleGetActionHandler, init),
    (r"/turtle/([^/]+)/response", handlers.TurtleResponseHandler, init),
    (r"/containers/get", handlers.ContainerGetHandler, init),
    (r"/containers/([^/]+)/put", handlers.ContainerPutHandler, init),
    (r"/containers/([^/]+)/take", handlers.ContainerTakeHandler, init),
    (r"/containers/([^/]+)/clear", handlers.ContainerClearHandler, init),
    (r"/containers/([^/]+)/set", handlers.ContainerSetHandler, init),
    (r"/logging/([^/]+)/(.*)", handlers.LoggingHandler, init),
    (r"/goals", handlers.GoalsListHandler, init),
    (r"/goals/add", handlers.GoalsAddHandler, init),
    (r"/goals/remove", handlers.GoalsRemoveHandler, init),
    (r"/resthelp", handlers.HelpHandler, init),
    (r"/listing",handlers.ListingHandler, init),
    (r"/startup",handlers.StartupHandler, init),
    (r"/static/(.*)", tornado.web.StaticFileHandler, {'path': 'static'})
  ]

  validator.setup({
    handlers.PathingQueryHandler: {
      "source": {
        "x":(int,float),
        "y":(int,float),
        "z":(int,float)
      },
      "destination": {
        "x":(int,float),
        "y":(int,float),
        "z":(int,float)
      }
    },
    handlers.PathingSetHandler: {
      "x":(int,float),
      "y":(int,float),
      "z":(int,float),
      "value":(int)
    },
    handlers.PathingGetHandler: {
      "x":(int,float),
      "y":(int,float),
      "z":(int,float)
    },
    handlers.RegisterTurtleHandler: {
      "x":(int,float),
      "y":(int,float),
      "z":(int,float),
      "facing":int,
    },
    handlers.UnregisterTurtleHandler: {
    },
    handlers.TurtleStatusHandler: { 
    },
    handlers.ListingHandler: {
    },
    handlers.TurtlePositionHandler: {
      "x":(int,float),
      "y":(int,float),
      "z":(int,float),
      "facing":int,
    },
    handlers.TurtleGetActionHandler: {
    },
    handlers.TurtleResponseHandler: {
    }, # Custom
    handlers.ContainerClearHandler: {
    },
    handlers.ContainerGetHandler: {
    },
    handlers.ContainerPutHandler: {
    },
    handlers.ContainerSetHandler: {
    },
    handlers.ContainerTakeHandler: {
    },
    handlers.GoalsAddHandler: {
      "goal":(str,unicode)
    },
    handlers.GoalsListHandler: {
    },
    handlers.GoalsRemoveHandler: {
    }
  }, routes)
    
  loader.load(os.path.curdir + "/test.yml")
  
  return (resolver, validator, tornado.web.Application(routes, **settings))

def start():
  resolver, validator, app = createApp()
  
  tornado.log.access_log.setLevel(logging.DEBUG)
  print(validator.dump())
  
  port = 34299
  app.listen(port)
  
  print("server listening on port {}".format(port))
  try:
    tornado.ioloop.IOLoop.instance().start()
  except KeyboardInterrupt:
    pass
  resolver.system.save()
