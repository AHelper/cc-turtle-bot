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
from cStringIO import StringIO

class RequestValidator:
  """
  templates is a dictionary of classes to templates.
  
  A template is a dictionary with keys and values.
  
  If the value is a dict, then it will traverse down.
  Else if the value is a type, then it will validate the type.
  Else, for any other value, it will do a comparison on the values.
  """
  def setup(self, templates, routes):
    self.templates = templates
    self.routes = {}
    
    for route in routes:
      self.routes[route[1]] = route[0]
    
  def __validate(self, template, json,path="/"):
    for key, value in template.iteritems():
      if key not in json:
        print("Key '{}' missing at {}".format(key, path))
        return False
      else:
        if type(value) == type:
          if type(json[key]) != value:
            print("{}/{} is not of type {}, found {}".format(path,key,value.__name__, type(json[key])))
            return False
        elif type(value) == tuple:
          for t in value:
            if type(json[key]) == t:
              break
          else:
            print("{}/{} is not any type required".format(path,key))
            return False
        elif type(value) == dict:
          if type(json[key]) != dict:
            return False
          if not self.__validate(value, json[key]):
            return False
        else:
          if value != json[key]:
            return False
    return True
  
  def validate(self, requestclass, json):
    if requestclass not in self.templates:
      raise KeyError()
    
    template = self.templates[requestclass]
    
    return self.__validate(template, json)
  
  def __dump(self, out, template, spaces):
      for key, value in template.iteritems():
        out.write(" "*spaces)
        out.write(key)
        out.write(": ")
        if type(value) == type:
          out.write("Must be type '")
          out.write(value.__name__)
          out.write("'\n")
        elif type(value) == tuple:
          out.write("Must be type ")
          out.write(", ".join(["'{}'".format(t.__name__) for t in value]))
          out.write("\n")
        elif type(value) == dict:
          out.write("\n")
          self.__dump(out, value, spaces+2)
        else:
          out.write(" Value must be '")
          out.write(value)
          out.write("'\n")
  def dump(self):
    out = StringIO()
    for requestclass, template in self.templates.iteritems():
      out.write(self.routes[requestclass])
      out.write(": Handler class is of type ")
      out.write(requestclass.__name__)
      out.write("\n")
      
      self.__dump(out, template, 2)
      out.write("\n")
      
    return out.getvalue()