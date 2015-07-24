os.loadAPI("log")
os.loadAPI("m")

function pathAlong(points)
  first = table.remove(points, 1)
  if m.x() ~= first[1] or m.y() ~= first[2] or m.z() ~= first[3] then
    log.error("I am not where I am supposed to be. Should be at "..v[1]..","..v[2]..","..v[3].." but am at "..m.x..","..m.y..","..m.z)
    return false
  end
  for k,v in pairs(points) do
    -- What direction must I go? Assume these are linear
    local facing = nil
    local move = 0
    if v[2] > m.y() then
      r=m.up(v[2]-m.y())
    elseif v[2] < m.y() then
      m.down(m.y-v[2])
    elseif v[1] > m.x() then
      facing = 2
      move = v[1] - m.x()
    elseif v[1] < m.x() then
      facing = 4
      move = m.x() - v[1]
    elseif v[3] > m.z() then
      facing = 1
      move = v[3] - m.z()
    elseif v[3] < m.z() then
      facing = 3
      move = m.z() - v[3]
    end
    
    -- TODO: Optimize movement
    if facing then
      while facing ~= m.facing() do
        log.debug("Now: "..tostring(m.facing()).." wants: "..tostring(facing))
        m.left()
      end
    end
    
    r = m.forward(move)
    if r ~= OK then
      return r
    end
    
    if m.x() ~= v[1] or m.y() ~= v[2] or m.z() ~= v[3] then
      log.error("I am not where I am supposed to be. Should be at "..v[1]..","..v[2]..","..v[3].." but am at "..m.x()..","..m.y()..","..m.z())
      return false
    end
  end
  return true
end

function test()
  m.load()
  dest = {
    x=-4,
    y=1,
    z=1
  }
  
  while m.x() ~= dest.x or m.y() ~= dest.y or m.z() ~= dest.z do
    log.debug("Trying to path")
    h=rest.post("pathing/query",{
      source={
        x=m.x(),
        y=m.y(),
        z=m.z()
      },
      destination=dest
    })
    j=textutils.unserialize(h:readAll())
    h:close()
    pathAlong(j.path)
  end
end