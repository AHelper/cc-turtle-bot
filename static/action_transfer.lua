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


os.loadAPI("blockmap")
os.loadAPI("itemmap")

-- ACTION: Transfers a block or item into an inventory
-- data:
--   direction: front, up, down
--   block|item: INT
--   count: INT

-- ISSUE: Front makes no sense, wtf is front?

function invoke(data)
  local name
  local toDrop = data.count
  local drop
  
  if data.location == "front" then
    drop = m.drop()
  elseif data.location == "up" then
    drop = m.dropUp()
  elseif data.location == "down" then
    drop = m.dropDown()
  else
    error("Unhandled transfer direction '"..data.direction.."'")
  end
  
  if data.block then
    name = blockmap.toName(data.block)
  elseif data.item then
    name = itemmap.toName(data.item)
  else
    error("Nothing specified to transfer")
  end
  
  for i=1,16,1 do    
    local info = turtle.getItemDetails(i)
    
    if info then
      if info.name == name then
        turtle.select(i)
        
      end
    end
  end
end