os.loadAPI("log")
os.loadAPI("m")

function pathAlong(points)
  first = table.remove(points, 1)
  if m.x ~= first[1] or m.y ~= first[2] or m.z ~= first[3] then
    log.error("I am not where I am supposed to be. Should be at "..v[1]..","..v[2]..","..v[3].." but am at "..m.x..","..m.y..","..m.z)
    return false
  end
  for k,v in pairs(points) do
    -- What direction must I go? Assume these are linear
    local facing = nil
    local move = 0
    if v[2] > m.y then
      m.up(v[2]-m.y)
    elseif v[2] < m.y then
      m.down(m.y-v[2])
    elseif v[1] > m.x then
      facing = 2
      move = v[1] - m.x
    elseif v[1] < m.x then
      facing = 4
      move = mx - v[1]
    elseif v[3] > m.z then
      facing = 1
      move = v[3] - m.z
    elseif v[3] < m.z then
      facing = 3
      move = m.z - v[3]
    end
    
    -- TODO: Optimize movement
    if facing then
      while facing ~= m.facing do
        log.debug("Now: "..tostring(m.facing).." wants: "..tostring(facing))
        m.left()
      end
    end
    
    m.forward(move)
    
    if m.x ~= v[1] or m.y ~= v[2] or m.z ~= v[3] then
      log.error("I am not where I am supposed to be. Should be at "..v[1]..","..v[2]..","..v[3].." but am at "..m.x..","..m.y..","..m.z)
      return false
    end
  end
  return true
end

function test()
  h=rest.post("pathing/query",{
    source={
      x=0,
      y=0,
      z=0
    },
    destination={
      x=2,
      y=0,
      z=0
    }
  })
  j=textutils.unserialize(h:readAll())
  h:close()
  pathAlong(j.path)
end