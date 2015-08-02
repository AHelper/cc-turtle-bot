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


import tornado.web
import tornado.escape
from cStringIO import StringIO

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