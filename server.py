#!/usr/bin/python

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
    #self.write(tornado.escape.json_encode(j))
    self.write(self.__jtos(j))
  def __jtos(self,v):
    if type(v) == int or type(v) == float:
      return str(v)
    elif type(v) == unicode or type(v) == str:
      return '"'+v+'"'
    elif type(v) == list or type(v) == tuple:
      return self.__jtos_l(v)
    elif type(v) == dict:
      return self.__jtos_d(v)
    elif v == None:
      return "null"
  def __jtos_d(self,j):
    s = StringIO()
    s.write("{")
    for k,v in j.iteritems():
      s.write(k+"=")
      s.write(self.__jtos(v))
      s.write(",")
    s.write("}")
    return s.getvalue()
  def __jtos_l(self,j):
    s = StringIO()
    s.write("{")
    for v in j:
      s.write(self.__jtos(v))
      s.write(",")
    s.write("}")
    return s.getvalue()
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
    
    if req["value"] == None:
      sys.pathing.set(int(req["x"]), int(req["y"]), int(req["z"]), None)
    else:
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

class TurtleActionHandler(JSONHandler):
  def get(self, id):
    if not sys.hasTurtle(id):
      raise HTTPError(404)
    else:
      self.write_json({"type":"success","action":sys.getTurtle(id).getCurrentTaskInfo()["action"],"data":sys.getTurtle(id).getCurrentTaskInfo()["data"]})
      
class TurtlePositionHandler(JSONHandler):
  def get(self, id):
    if not sys.hasTurtle(id):
      raise HTTPError(404)
    else:
      t = sys.getTurtle(id)
      self.write_json(t.getPosition())
  def post(self, id):
    if not sys.hasTurtle(id):
      raise HTTPError(404)
    else:
      req = self.read_json()
      if not validator.validate(TurtlePositionHandler, req):
        raise HTTPError(400)
      else:
        t = sys.getTurtle(id)
        t.setPosition(req["x"],req["y"],req["z"],req["facing"])
        self.write_json({"type":"success"})
      
class ListingHandler(JSONHandler):
  def get(self):
    os.chdir('static')
    list = glob('*.lua')
    os.chdir('..')
    
    self.write("\n".join(list))
    
class StartupHandler(JSONHandler):
  def get(self):
    self.write("core")
    
class LoggingHandler(JSONHandler):
  def post(self, id, level):
    level = int(level)
    tornado.log.app_log.setLevel(logging.DEBUG)
    if level <= 2:
      tornado.log.app_log.critical("{}: {}".format(id,self.request.body))
    elif level == 3:
      tornado.log.app_log.error("{}: {}".format(id,self.request.body))
    elif level == 4:
      tornado.log.app_log.warning("{}: {}".format(id,self.request.body))
    elif level == 5 or level == 6:
      tornado.log.app_log.info("{}: {}".format(id,self.request.body))
    elif level == 7:
      tornado.log.app_log.debug("{}: {}".format(id,self.request.body))
      
settings = {
  'default_handler_class': JSONErrorHandler,
  'default_handler_args': dict(status_code=404),
  'debug': True
}

routes = [
  (r"/pathing/get", PathingGetHandler),
  (r"/pathing/set", PathingSetHandler),
  (r"/pathing/query", PathingQueryHandler),
  (r"/turtle/([^/]+)/register", RegisterTurtleHandler),
  (r"/turtle/([^/]+)/unregister", UnregisterTurtleHandler),
  (r"/turtle/([^/]+)/status", TurtleStatusHandler),
  (r"/turtle/([^/]+)/position", TurtlePositionHandler),
  (r"/logging/([^/]+)/(.*)", LoggingHandler),
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
  },
  TurtlePositionHandler: {
    "x":(int,float),
    "y":(int,float),
    "z":(int,float),
    "facing":int,
  }
}, routes)
app = tornado.web.Application(routes, **settings)

if __name__ == '__main__':
  print(validator.dump())
  port = 34299
  app.listen(port)
  print("server listening on port {}".format(port))
  print(dir(tornado.log.access_log))
  tornado.log.access_log.setLevel(logging.DEBUG)
  try:
    tornado.ioloop.IOLoop.instance().start()
  except KeyboardInterrupt:
    pass
  sys.pathing.save()
  