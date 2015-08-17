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


from ccturtle.system import SQLiteStorageItem

class Building(SQLiteStorageItem):
  def __init__(self, x, y, z, building_type, mk=1, id=None):
    self.x = x
    self.y = y
    self.z = z
    self.building_type = building_type
    self.mk = mk
    self.id = id
    
  def sql(self):
    return (self.id, self.x, self.y, self.z, self.building_type, self.mk)
  
  @staticmethod
  def args(self):
    return "id x y z building_type mk".split(" ")