os.loadAPI("path")
os.loadAPI("log")

-- ACTION: Discovers an 8x8xn volume at the current location
-- data:
--   height: INT
--   x: INT
--   y: INT
--   z: INT


-- local detected = {}
local openPoints = {}
local closedPoints = {}

-- local function getKey()
--   return tostring(m.x())..":"..tostring(m.y())..":"..tostring(m.z())
-- end
-- 
-- local function mark()
--   detected[getKey()] = true
-- end

local function mark(x,y,z,sx,sy,sz,h)
  table.insert(closedPoints, {x,y,z})
  if x ~= sx   then table.insert(openPoints,{x-1,y,z}) end
  if x ~= sx+7 then table.insert(openPoints,{x+1,y,z}) end
  if y ~= sy   then table.insert(openPoints,{x,y-1,z}) end
  if y ~= sy+7 then table.insert(openPoints,{x,y+1,z}) end
  if z ~= sz   then table.insert(openPoints,{x,y,z-1}) end
  if z ~= sz+7 then table.insert(openPoints,{x,y,z+1}) end
end

function invoke(data)
  -- Clear out the region
  log.debug("Clearing region")
  for y=data.y,data.y+data.height,1 do
    for x=data.x,data.x+8,1 do
      for z=data.z,data.z+8,1 do
        rest.post("pathing/set",{
          x=x,
          y=y,
          z=z,
          value=nil
        }, true)
      end
    end
  end
  -- Loop to every point in the region and go there
  log.debug("Discovering region")
  for y=data.y,data.y+data.height,1 do
    for x=data.x,data.x+8,1 do
      for z=data.z,data.z+8,1 do
        while not rest.api.pathing.get(x,y,z) do
          local points = rest.api.pathing.query(x,y,z,m.x(),m.y(),m.z())
          
          if points then
            local points = rest.api.pathing.query(m.x(),m.y(),m.z(),x,y,z)
            log.debug("Got points")
            if path.pathAlong(points) then
              log.debug("Pathed")
              break
            end
          else
            break
          end
        end
      end
    end
  end
end

