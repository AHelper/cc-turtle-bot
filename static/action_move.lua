os.loadAPI("rest")
os.loadAPI("path")
os.loadAPI("log")

-- ACTION: Moves to a location
-- data:
--   x: INT
--   y: INT
--   z: INT
--   tries: INT

local function doMove(data)
  local path = rest.api.pathing.query(m.x(),m.y(),m.z(),data.x,data.y,data.z)
  
  if path then
    return path.pathAlong(path)
  else
    return false
  end
end

function invoke(data)
  for try=0,data.tries,1 do
    local r = doMove(data)
    if r then
      return true
    end
  end
  return false
end
