os.loadAPI("path")
os.loadAPI("log")

-- ACTION: Discovers an 8x8xn volume at the current location
-- data:
--   height: INT
--   x: INT
--   y: INT
--   z: INT


local detected = {}

local function getKey()
  return tostring(m.x())..":"..tostring(m.y())..":"..tostring(m.z())
end

local function mark()
  detected[getKey()] = true
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
            if path.pathAlong(points) then
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

