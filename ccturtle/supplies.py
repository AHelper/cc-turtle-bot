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


from ccturtle.sqlitestorageitem import SQLiteStorageItem

class Container(SQLiteStorageItem):
  TURTLE = 1
  CHEST  = 2
  
  def __init__(self, id, type, x=None, y=None, z=None, turtleid=None):
    self.storage = {}
    
  def save(self, sql):
    cur = sql.getCursor()
    cur.execute("INSERT OR REPLACE INTO containers (id, type, x, y, z, turtleid) VALUES (?,?,?,?,?,?)", (self.id, self.type, self.x, self.y, self.z, self.turtleid))
    sql.commit()
    
  @staticmethod
  def load(id, sql):
    cur = sql.getCursor()
    cur.execute("SELECT id, type, x, y, z, turtleid FROM containers WHERE id = ?", (id,))
    
    row = cur.fetchone()
    
    if row:
      return Container(row[0], row[1], x=row[2], y=row[3], z=row[4], turtleid=row[5])
    else:
      return None
  
  @staticmethod
  def destroy(id, sql):
    cur = sql.getCursor()
    cur.execute("DELETE FROM containers WHERE id = ?", (id,))
    sql.commit()
    
  def fromAction(self):
    return False
  
  def fromTop(self):
    return False
  
  def fromBottom(self):
    return False
  
  def fromSide(self):
    return False
  
  def getType(self):
    return self.type
  
  def getPos(self):
    return self.pos
  
  def getId(self):
    return self.id
  
  def clear(self):
    resources = Resource.loadAllFor(self)
    
    for resource in resources:
      resource.setCount(0)
      resource.save()
  
class Resource:
  @staticmethod
  def loadAllFor(container, sql):
    pass
  
  @staticmethod
  def merge(sql):
    '''
    Merges same resources for same containers into single resources
    '''
    pass
  
  def save(self):
    '''
    Potentially deletes this from SQL if count == 0
    '''
    pass
  
  def getType(self):
    pass
  
  def getCount(self):
    pass
  
  def getContainer(self):
    pass
  
  def setCount(self):
    pass
  