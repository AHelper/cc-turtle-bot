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
    if v[2] > m.y then
      m.up(v[2]-m.y)
    elseif v[2] < m.y then
      m.down(m.y-v[2])
    elseif v[1] > m.x then
      facing = 2
    elseif v[1] < m.x then
      facing = 4
    elseif v[3] > m.z then
      facing = 1
    elseif v[3] < m.z then
      facing = 3
    end
    
    if facing then
      while facing ~= m.facing do
        m.tu
      end
    end
    
    if m.x ~= v[1] or m.y ~= v[2] or m.z ~= v[3] then
      log.error("I am not where I am supposed to be. Should be at "..v[1]..","..v[2]..","..v[3].." but am at "..m.x..","..m.y..","..m.z)
      return false
    end
    
  end
end