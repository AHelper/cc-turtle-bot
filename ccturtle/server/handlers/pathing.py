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


from tornado.web import HTTPError
from ccturtle.server.json import JSONHandler

class PathingQueryHandler(JSONHandler):
  def initialize(self, sys):
    self.sys = sys
    
  def post(self):
    req = self.read_json()
    if type(req) == dict:
      if not req.has_key("source") or not req.has_key("destination"):
        raise HTTPError(400)
    else:
      raise HTTPError(400)
    
    path = self.sys.pathing.pathSearch((int(req["source"]["x"]), int(req["source"]["y"]), int(req["source"]["z"])), (int(req["destination"]["x"]), int(req["destination"]["y"]), int(req["destination"]["z"])))
    
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