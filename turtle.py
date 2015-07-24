
"""
Control entrypoint for a single turtle.
"""
class Turtle:
  def __init__(self, unique_name, x, y, z, facing):
    self.x = x
    self.y = y
    self.z = z
    self.facing = facing
    self.name = unique_name
    
    self.designation = None
  
  def getName(self):
    return self.name
  
  def setDesignation(self, designation):
    self.designation = designation
    
  def getDesignation(self):
    return self.designation
  
  def think(self):
    """
    Figures out what to do
    """
    pass
  
  def handleResponse(self, response):
    """
    Handles a response from the Lua code
    """
    pass
  
  def setPosition(self, x, y, z, facing):
    self.x = x
    self.y = y
    self.z = z
    self.facing = facing
    
  def getPosition(self):
    return {
      "x":self.x,
      "y":self.y,
      "z":self.z,
      "facing":self.facing
    }
  
  def getResponse(self):
    """
    Generates a response for the turtle for what it should do
    """
    pass
  
  def getCurrentTaskInfo(self):
    pass
  
  def getHumanReadableCurrentTask(self):
    return "Faffing about"
  
  def getHumanReadableFutureTasks(self):
    return "More faffing about"
  