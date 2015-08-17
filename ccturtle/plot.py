from ccturtle.system import SQLiteStorageItem
class Plot(SQLiteStorageItem):
  def __init__(self, x, y, z, id=None):
    self.x = x
    self.y = y
    self.z = z
    self.id = id
    
  def sql(self):
    return (self.id, self.x, self.y, self.z)
  
  @staticmethod
  def args(self):
    return "id x y z".split(" ")