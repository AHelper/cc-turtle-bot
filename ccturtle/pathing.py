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


import octree
import os
import math

class Pathing:
  def __init__(self):
    self.octrees = {}
    self.size = 256
    self.basepath = "/opt/chunks/"
    
  def save(self):
    if not os.path.isdir(self.basepath):
      os.mkdir(self.basepath)
    for k, o in self.octrees.iteritems():
      o.save(self.basepath+"{}.o".format(k))
  
  def __lookupoctree(self,x,y,z):
    key = "{},{},{}".format(x/self.size,y/self.size,z/self.size)
    
    if key not in self.octrees:
      self.octrees[key] = octree.octree(self.size)
      path = self.basepath+"{}.o".format(key)
      
      if os.path.exists(path):
        self.octrees[key].load(path)
    
    return self.octrees[key]
    
  def set(self,x,y,z,v):
    o = self.__lookupoctree(x,y,z)
    
    o.setPoint(x%self.size,y%self.size,z%self.size,v)
  
  def get(self,x,y,z):
    o = self.__lookupoctree(x,y,z)
    
    return o.getPoint(x%self.size,y%self.size,z%self.size)
  
  # Need A* algorithm with an eliminator function
  def pathSearch(self, start, end):
    #for index, node in enumerate(nodes):
      #if type(start) == tuple and node[0] == start[0] and node[1] == start[1]:
        #start = index
      #if type(end) == tuple and node[0] == end[0] and node[1] == end[1]:
        #end = index
      #if type(start) == int and type(end) == int:
        #break
    
    nodes = {}
    
    # Parent, score
    #nodes[start] = (None)
    #nodes[end] = (None)
    
    openSet = []
    closedSet = []
    
    ## A* Vertex Updater
    #def updateVertex(current, next, start, end, walls, open):
      ##print('{} < {}'.format(current[3] + c(current, next), next[3]))
      ## if g(s) + c(s, s`) < g(s)
      #if current[3] + c(current, next) < next[3]:
        #next[3] = current[3] + c(current, next)
        #next[4] = current
        
        #if next not in open:
          #open.append(next)
        #open.sort(key=lambda node: node[3] + c(node,end), reverse=True)
      
    def c(n1, n2):
      return math.sqrt((n1.x-n2.x)*(n1.x-n2.x)+(n1.y-n2.y)*(n1.y-n2.y)+(n1.z-n2.z)*(n1.z-n2.z))
    
    def h(n):
      return c(n, nodes[end])
    
    def calcHeading(n1,n2): # from, to
      if n2.z > n1.z:
        return 0
      elif n2.x > n1.x:
        return 1
      elif n2.z < n1.z:
        return 2
      elif n2.x < n1.x:
        return 3
      return n1.direction
    
    def calcHeadingScore(a,b):
      if a == None or b == None:
        return 0
      elif a == b:
        return 0
      elif ((a+1)%4) == b or a == ((b+1)%4):
        return 1
      else:
        return 2
      
    class Node:
      def __init__(self,xyz,parent,super):
        self.xyz = xyz
        self.x, self.y, self.z = xyz
        self.parent = parent
        if parent == end:
          self.score = 0
          self.scoreg = 0
          self.direction = None
        elif parent != None:
          self.scoreg = self.parent.scoreg
          self.direction = calcHeading(self.parent, self) # TODO: Calculate
          self.scoreg += calcHeadingScore(self.parent.direction, self.direction)
          self.score = self.scoreg + h(self)
        else:
          self.scoreg = 0
          self.direction = None
          self.score = h(self)
        self.super = super
        self.value = super.get(*xyz)
      def __lt__(self, other):
        return other.score >= self.score
      def neighbors(self):
        # Get 6 neighbors by xyz tuple
        nl = [
          (self.x, self.y, self.z+1),
          (self.x, self.y, self.z-1),
          (self.x, self.y+1, self.z),
          (self.x, self.y-1, self.z),
          (self.x+1, self.y, self.z),
          (self.x-1, self.y, self.z),
        ]
        
        ret = []
        
        for n in nl:
          if n not in nodes:
            nodes[n] = Node(n, self, self.super)
            
          if nodes[n].value == 0 or nodes[n].value == None:
            ret.append(nodes[n])
            
        return ret
        
    #nodes[start][3] = h(nodes[start])
    nodes[end] = Node(end, end, self)
    nodes[start] = Node(start, None, self)
    openSet.append(nodes[start])
    step = 0
    
    ###################################
    while len(openSet) > 0:
      node = openSet.pop()
      
      #print("Open set is {} with node at {},{},{} {}".format(len(openSet), node.x,node.y,node.z,node.score))
      step += 1
      if node == nodes[end]:
        print("Found path")
        break
      else:
        closedSet.append(node)
        for neighbor in node.neighbors():
          if neighbor not in closedSet:
            if neighbor not in openSet:
              neighbor.parent = node
              openSet.append(neighbor)
              openSet.sort(reverse=True)
            #updateVertex(node, neighbor, nodes[start], nodes[end], walls, openSet)
    else:
      return None
    
    # Walk back
    ret = []
    while node != None:
      #print("Resolving")
      ret.append(node.xyz)
      node = node.parent
    ret.reverse()
    return ret
  ## A* Vertex Updater
  #def astarUpdate(current, next, start, end, walls, open):
    ##print('{} < {}'.format(current[3] + c(current, next), next[3]))
    ## if g(s) + c(s, s`) < g(s)
    #if current[3] + c(current, next) < next[3]:
      #next[3] = current[3] + c(current, next)
      #next[4] = current
      
      #if next not in open:
        #open.append(next)
      #open.sort(key=lambda node: node[3] + c(node,end), reverse=True)