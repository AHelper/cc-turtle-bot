#!/usr/bin/python

'''
Documentation, License etc.

@package turtle
'''

import tornado.escape
import tornado.ioloop
import tornado.web

import pathing
from requestparser import RequestValidator

validator = RequestValidator()

class System:
  def __init__(self):
    self.pathing = pathing.Pathing()

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

class PathingGetHandler(JSONHandler):
  def post(self):
    req = self.read_json()
    if type(req) == dict:
      if not req.has_key("source") or not req.has_key("destination"):
        raise tornado.web.HTTPError(400)
    else:
      raise tornado.web.HTTPError(400)
    
    self.write_json({"response":"not_implemented","message":"Pathing module not implemented"})

class PathingSetHandler(JSONHandler):
  def post(self):
    req = self.read_json()
    
    sys.pathing.set(int(req["x"]), int(req["y"]), int(req["z"]), int(req["value"]))
    
    self.write_json({"response":"success","message":"point set"})

class PathingQueryHandler(JSONHandler):
  def post(self):
    req = self.read_json()
    
    self.write_json({"type":"success","value":sys.pathing.get(int(req["x"]), int(req["y"]), int(req["z"]))})
    
settings = {
  'default_handler_class': JSONErrorHandler,
  'default_handler_args': dict(status_code=404)
}

routes = [
  (r"/pathing/get", PathingGetHandler),
  (r"/pathing/set", PathingSetHandler),
  (r"/pathing/query", PathingQueryHandler),
  (r"/resthelp", HelpHandler),
  (r"/static/(.*)", tornado.web.StaticFileHandler, {'path': 'static'})
]

validator.setup({
  PathingGetHandler: {
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
  PathingQueryHandler: {
    "x":(int,float),
    "y":(int,float),
    "z":(int,float)
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
  