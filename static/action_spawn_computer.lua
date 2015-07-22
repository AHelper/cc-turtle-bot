os.loadAPI("m")
os.loadAPI("rest")

-- ACTION REQs:

-- Turtle must be in front of a floppy drive with floppy in it
-- Turtle must have computer/turtle

local function place(inv)
  m.up(1)
  m.place(inv)
  id = m.getId()
  pos = m.getRel()
  
  h = rest.post("turtle/"..id.."/register",
    {
      "x":pos.x,
      "y":pos.y,
      "z":pos.z,
      "facing":pos.facing
    })
  
  if h == nil then
    error("Can't register turtle!")
  end
  
  m.on()
  m.down(1)
end

function invoke(data)
  local inv = -1
  if data.type == "turtle" then
    inv = m.findG("turtle") -- TODO: ID of turtle
    -- TODO: One for each type of turtle
  else
    inv = m.findG("computer") -- TODO: ID of computer
  end
  
  if inv ~= -1 then
    m.begin()
    if pcall(place, inv) then
      m.finish()
      log.info("
    else
      m.revert()
    end
  else
    
  end