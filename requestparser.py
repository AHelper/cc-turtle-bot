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
    
  def __validate(self, template, json):
    for key, value in template.iteritems():
      if key not in json:
        return False
      else:
        if type(value) == type:
          if type(json[key]) != value:
            return False
        elif type(value) == tuple:
          for t in value:
            if type(json[key]) != t:
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