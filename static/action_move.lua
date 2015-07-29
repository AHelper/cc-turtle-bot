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
