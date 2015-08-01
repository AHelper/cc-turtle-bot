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


import struct

class octree:
  def __init__(self,s):
    self.s = s
    self.ptrarray = [None,None,None,None,None,None,None,None]
  
  def dumpPtrs(self,out,ptrs):
    for d in ptrs:
      if type(d) == list:
        i = 0xFF
      elif d == None:
        i = 0xFE
      else:
        i = d
      out.write(struct.pack('B',i))
    for d in ptrs:
      if type(d) == list:
        self.dumpPtrs(out, d)
    
  def save(self,path):
    out = open(path,'wb')
    self.dumpPtrs(out,self.ptrarray)
    out.close()
  
  def loadPtrs(self,f):
    l = list(struct.unpack('8B',f.read(8)))
    for i in range(0,len(l)):
      if l[i] == 0xFF:
        l[i] = self.loadPtrs(f)
      elif l[i] == 0xFE:
        l[i] = None
    return l
    
  def load(self,path):
    f = open(path,'rb')
    self.ptrarray = self.loadPtrs(f)
  
  def setPoint(self,x,y,z,v):
    self.__setPoint(x,z,y,v,self.ptrarray,0,0,0,self.s)
    
  def __setPoint(self,x,y,z,v,ptrs,lx,ly,lz,s):
    h = s / 2
    m = (0b001 if x >= lx + h else 0) | (0b010 if y >= ly + h else 0) | (0b100 if z >= lz + h else 0)
    
    d = ptrs[m]
    
    if m & 0b001:
      lx += h
    if m & 0b010:
      ly += h
    if m & 0b100:
      lz += h
      
    if type(d) == list:
      self.__setPoint(x,y,z,v,d,lx,ly,lz,s/2)
    elif s != 2:
      # This is a leaf node, but not the end of the line
      ptrs[m] = [d]*8
      self.__setPoint(x,y,z,v,ptrs[m],lx,ly,lz,s/2)
    else:
      # End of the line!
      ptrs[m] = v
    
    # TODO: If ptrs is all the same value, collape into one
  
  def getPoint(self,x,y,z):
    return self.__getPoint(x,z,y,self.ptrarray,0,0,0,self.s)
    
  def __getPoint(self,x,y,z,ptrs,lx,ly,lz,s):
    h = s / 2
    m = (0b001 if x >= lx + h else 0) | (0b010 if y >= ly + h else 0) | (0b100 if z >= lz + h else 0)
    
    d = ptrs[m]
    
    if m & 0b001:
      lx += h
    if m & 0b010:
      ly += h
    if m & 0b100:
      lz += h
      
    #print(m,type(d),lx,ly,lz,s,h)
    if type(d) == list:
      return self.__getPoint(x,y,z,d,lx,ly,lz,s/2)
    else:
      # Leaf node!
      return d
