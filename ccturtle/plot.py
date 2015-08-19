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

class Plot(SQLiteStorageItem):
  def __init__(self, x, y, z, id=None):
    self.x = x
    self.y = y
    self.z = z
    self.id = id
    
  def sql(self):
    return (self.id, self.x, self.y, self.z)
  
  @staticmethod
  def args():
    return "id x y z".split(" ")