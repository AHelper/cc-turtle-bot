os.loadAPI("m")
os.loadAPI("blockmap")

-- ACTION: Collects block(s) around the turtle.
-- data:
--   id: INT block ID

local function collect(inspect, dig, name)
  local info = inspect()
  
  if info then
    if info.name == name then
      dig()
    end
  end
end

function invoke(data)
  local id = blockmap.toName(data.id)
  
  collect(m.inspectUp, m.digUp, id)
  collect(m.inspectDown, m.digDown, id)
  collect(m.inspect, m.dig, id)
  m.left()
  collect(m.inspect, m.dig, id)
  m.left()
  collect(m.inspect, m.dig, id)
  m.left()
  collect(m.inspect, m.dig, id)
end