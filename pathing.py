import octree
import os

class Pathing:
  def __init__(self):
    self.octrees = {}
    self.size = 256
  
  def __lookupoctree(self,x,y,z):
    key = "{},{},{}".format(x/self.size,y/self.size,z/self.size)
    
    if key not in self.octrees:
      self.octrees[key] = octree.octree(self.size)
      path = "chunks/{}.o".format(key)
      
      if os.path.exists(path):
        self.octrees[key].load(path)
    
    return self.octrees[key]
    
  def set(self,x,y,z,v):
    o = self.__lookupoctree(x,y,z)
    
    o.setPoint(x,y,z,v)
  
  def get(self,x,y,z):
    o = self.__lookupoctree(x,y,z)
    
    return o.getPoint(x,y,z)
  
  