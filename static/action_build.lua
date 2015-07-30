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


os.loadAPI("config")
os.loadAPI("rest")

-- ACTION: Builds a structure starting at its current position
-- data:
--   name: STR (Name of the building)

-- Returns an iterator function that returns a map:
-- type:
--   header:
--     key: STR
--     value: STR
--   slice
--     position: x, y, z
--     size: w, h
--     blocks: [[INT, INT, INT]]
local function parseBuilding(building)
  local state = 1
  -- 1: headers
  -- 2: slices
  return function()
    if state == 1 then
      
    elseif state == 2 then
      
    end
  end
end

function invoke(data)
  -- Get the schematic
  if not data.name then
    error("Missing building name")
  end
  
  local building = rest.get(config.building_base_url + data.name + ".building")
  
  
end