--  cc-turtle-bot
--  Copyright (C) 2015 Collin Eggert
--  
--  This program is free software: you can redistribute it and/or modify
--  it under the terms of the GNU General Public License as published by
--  the Free Software Foundation, either version 3 of the License, or
--  (at your option) any later version.
--  
--  This program is distributed in the hope that it will be useful,
--  but WITHOUT ANY WARRANTY; without even the implied warranty of
--  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
--  GNU General Public License for more details.
--  
--  You should have received a copy of the GNU General Public License
--  along with this program.  If not, see <http://www.gnu.org/licenses/>.


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
      x=pos.x,
      y=pos.y,
      z=pos.z,
      facing=pos.facing
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
    inv = m.find("turtle") -- TODO: ID of turtle
    -- TODO: One for each type of turtle
  else
    inv = m.find("computer") -- TODO: ID of computer
  end
  
  if inv then
    m.setError(true)
    if pcall(place, inv) then
      m.finish()
      log.info("Spawned turtle")
      rest.get("turtle/"..config.id.."/success", true)
    else
      log.error("Could not spawn turtle")
      rest.get("turtle/"..config.id.."/failure", true)
    end
    m.setError(false)
  else
    log.error("Don't have needed blocks")
    rest.get("turtle/"..config.id.."/failure", true)
  end
end