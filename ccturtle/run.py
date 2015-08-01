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


#!/usr/bin/python

import octree

o=octree.octree(16)
o.setPoint(0,0,0,1)
o.setPoint(0,0,1,2)
o.setPoint(0,1,0,3)
o.setPoint(0,1,1,4)
o.setPoint(1,0,0,5)
o.setPoint(1,0,1,6)
o.setPoint(1,1,0,7)
o.setPoint(1,1,1,8)
o.save('test1.o')

print(o.getPoint(0,0,0))
print(o.getPoint(0,0,1))
print(o.getPoint(0,1,0))
print(o.getPoint(0,1,1))
print(o.getPoint(1,0,0))
print(o.getPoint(1,0,1))
print(o.getPoint(1,1,0))
print(o.getPoint(1,1,1))
