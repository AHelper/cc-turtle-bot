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
os.loadAPI("blockmap")
os.loadAPI("log")

-- ACTION: Collects block(s) around the turtle.
-- data:
--   id: INT block ID

local function collect(inspect, dig, name)
  local info = inspect()
  
  if info then
    log.debug("Found "..info.name)
    if info.name == name then
      log.debug("Trying to dig")
      local ok = dig()
      if not ok then log.error("Failed to dig it") end
    end
  end
end

function invoke(data)
  local id = blockmap.toName(data.id)
  
  if id then
    log.debug("Collecting " .. id)
    collect(m.inspectUp, m.digUp, id)
    collect(m.inspectDown, m.digDown, id)
    collect(m.inspect, m.dig, id)
    m.left()
    collect(m.inspect, m.dig, id)
    m.left()
    collect(m.inspect, m.dig, id)
    m.left()
    collect(m.inspect, m.dig, id)
  else
    error("Invalid id " .. tostring(data.id))
  end
end