#!/usr/bin/python

'''
Documentation, License etc.

@package turtle
'''

import tornado.escape
import tornado.ioloop
import tornado.web
from tornado.web import HTTPError

from glob import glob
import os

import pathing
from requestparser import RequestValidator
from turtle import Turtle

validator = RequestValidator()

class System:
  def __init__(self):
    self.pathing = pathing.Pathing()
    self.turtles = {}
    
  def addTurtle(self, turtle):
    self.turtles[turtle.getName()] = turtle
    
  def getTurtle(self, name):
    return self.turtles[name]
  
  def delTurtle(self, name):
    del self.turtles[name]
  
  def hasTurtle(self, name):
    return self.turtles.has_key(name)

sys = System()

class HelpHandler(tornado.web.RequestHandler):
  def get(self):
    self.write(validator.dump())

class JSONHandler(tornado.web.RequestHandler):
  def write_error(self, status_code, **kwargs):
    self.write(tornado.escape.json_encode({"type":"error","message":"error code {}".format(status_code)}))
  def write_json(self, j):
    self.write(tornado.escape.json_encode(j))
  def read_json(self):
    try:
      return tornado.escape.json_decode(self.request.body)
    except:
      raise tornado.web.HTTPError(400)
    
class JSONErrorHandler(tornado.web.ErrorHandler, JSONHandler):
  pass

class PathingQueryHandler(JSONHandler):
  def post(self):
    req = self.read_json()
    if type(req) == dict:
      if not req.has_key("source") or not req.has_key("destination"):
        raise HTTPError(400)
    else:
      raise tornado.web.HTTPError(400)
    
    path = sys.pathing.pathSearch((int(req["source"]["x"]), int(req["source"]["y"]), int(req["source"]["z"])), (int(req["destination"]["x"]), int(req["destination"]["y"]), int(req["destination"]["z"])))
    
    if not path:
      self.write_json({"type":"failure","message":"Path not found"})
    else:
      self.write_json({"type":"success","path":path})

class PathingSetHandler(JSONHandler):
  def post(self):
    req = self.read_json()
    
    sys.pathing.set(int(req["x"]), int(req["y"]), int(req["z"]), int(req["value"]))
    
    self.write_json({"response":"success","message":"point set"})

class PathingGetHandler(JSONHandler):
  def post(self):
    req = self.read_json()
    
    self.write_json({"type":"success","value":sys.pathing.get(int(req["x"]), int(req["y"]), int(req["z"]))})
    
class RegisterTurtleHandler(JSONHandler):
  def post(self, name):
    req = self.read_json()
    if not validator.validate(RegisterTurtleHandler, req):
      print("Failed to validate")
      raise HTTPError(400)
    
    if not sys.hasTurtle(name):
      sys.addTurtle(Turtle(name, req['x'], req['y'], req['z'], req['facing']))
      self.write_json({"type":"success"})
    else:
      self.write_json({"type":"failure","message":"turtle alread exists"})
      
class UnregisterTurtleHandler(JSONHandler):
  def post(self, name):    
    if not sys.hasTurtle(name):
      sys.delTurtle(name)
      self.write_json({"type":"success"})
    else:
      self.write_json({"type":"failure","message":"turtle alread exists"})
      
class TurtleStatusHandler(JSONHandler):
  def get(self, turtle_name):
    if not sys.hasTurtle(turtle_name):
      raise HTTPError(404)
    else:
      self.write_json({"type":"success","current":sys.getTurtle(turtle_name).getHumanReadableCurrentTask(),"future":sys.getTurtle(turtle_name).getHumanReadableFutureTasks()})

class ListingHandler(JSONHandler):
  def get(self):
    os.chdir('static')
    list = glob('*.lua')
    os.chdir('..')
    
    self.write("\n".join(list))
    
class StartupHandler(JSONHandler):
  def get(self):
    self.write("core")
    
settings = {
  'default_handler_class': JSONErrorHandler,
  'default_handler_args': dict(status_code=404)
}

routes = [
  (r"/pathing/get", PathingGetHandler),
  (r"/pathing/set", PathingSetHandler),
  (r"/pathing/query", PathingQueryHandler),
  (r"/turtles/([^/]+)/register", RegisterTurtleHandler),
  (r"/turtles/([^/]+)/unregister", UnregisterTurtleHandler),
  (r"/turtles/([^/]+)/status", TurtleStatusHandler),
  (r"/resthelp", HelpHandler),
  (r"/listing",ListingHandler),
  (r"/startup",StartupHandler),
  (r"/static/(.*)", tornado.web.StaticFileHandler, {'path': 'static'})
]

validator.setup({
  PathingQueryHandler: {
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
  PathingSetHandler: {
    "x":(int,float),
    "y":(int,float),
    "z":(int,float),
    "value":(int)
  },
  PathingGetHandler: {
    "x":(int,float),
    "y":(int,float),
    "z":(int,float)
  },
  RegisterTurtleHandler: {
    "x":(int,float),
    "y":(int,float),
    "z":(int,float),
    "facing":int,
  },
  UnregisterTurtleHandler: {
  },
  TurtleStatusHandler: { 
  },
  ListingHandler: {
  }
}, routes)
app = tornado.web.Application(routes, **settings)

if __name__ == '__main__':
  print(validator.dump())
  port = 34299
  app.listen(port)
  print("server listening on port {}".format(port))
  try:
    tornado.ioloop.IOLoop.instance().start()
  except KeyboardInterrupt:
    pass
  