os.loadAPI("log")
os.loadAPI("m")

function pathAlong(points)
  for k,v in pairs(points) do
    if m.x ~= v[1] or m.y ~= v[2] or m.z ~= v[3] then
      log.error("I am not where I am supposed to be. Should be at "..v[1]..","..v[2]..","..v[3].." but am at "..m.x..","..m.y..","..m.z)
      return false
    else
      -- What direction must I go? Assume these are linear
      if v[2] > m.y then
        
    end
  end
end