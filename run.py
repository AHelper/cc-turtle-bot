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
