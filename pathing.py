import octree
import os
import math

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
  
  # Need A* algorithm with an eliminator function
  def __pathSearch(self, nodes, walls, start, end):
    #for index, node in enumerate(nodes):
      #if type(start) == tuple and node[0] == start[0] and node[1] == start[1]:
        #start = index
      #if type(end) == tuple and node[0] == end[0] and node[1] == end[1]:
        #end = index
      #if type(start) == int and type(end) == int:
        #break
    
    nodes = {}
    
    # Parent, score
    nodes[start] = (None)
    nodes[end] = (None)
    
    openSet = []
    closedSet = []
    
    # A* Vertex Updater
    def updateVertex(current, next, start, end, walls, open):
      #print('{} < {}'.format(current[3] + c(current, next), next[3]))
      # if g(s) + c(s, s`) < g(s)
      if current[3] + c(current, next) < next[3]:
        next[3] = current[3] + c(current, next)
        next[4] = current
        
        if next not in open:
          open.append(next)
        open.sort(key=lambda node: node[3] + c(node,end), reverse=True)
      
    def c(n1, n2):
      return math.sqrt((n1[0]-n2[0])*(n1[0]-n2[0])+(n1[1]-n2[1])*(n1[1]-n2[1]))
    
    def h(n):
      return c(n, nodes[end])
    
    class NodeScorePair:
      def __init__(self,ref,parent):
        self.ref = ref
        self.score = parent.score + h(ref,parent)
      def __lt__(self, other):
        return other.score < self.score
    
    nodes[start][3] = h(nodes[start])
    openSet.append(nodes[start])
    step = 0
    
    ###################################
    while len(openSet) > 0:
      node = openSet.pop()
      
      step += 1
      
      if node== nodes[end]:
        print("Found path")
        break
      else:
        closedSet.append(node)
        for neighbor in node[2]:
          if neighbor not in closedSet:
            if neighbor not in openSet:
              neighbor[3] = float('inf')
              neighbor[4] = None
            updateVertex(node, neighbor, nodes[start], nodes[end], walls, openSet)

  # A* Vertex Updater
  def astarUpdate(current, next, start, end, walls, open):
    #print('{} < {}'.format(current[3] + c(current, next), next[3]))
    # if g(s) + c(s, s`) < g(s)
    if current[3] + c(current, next) < next[3]:
      next[3] = current[3] + c(current, next)
      next[4] = current
      
      if next not in open:
        open.append(next)
      open.sort(key=lambda node: node[3] + c(node,end), reverse=True)