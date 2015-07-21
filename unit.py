import pathing

p = pathing.Pathing()
assert p.get(1,0,0) == None
p.set(1,0,0,1)
assert p.get(1,0,0) == 1

s = (0,0,0)
e = (100,0,0)
print(p.pathSearch(s, e))