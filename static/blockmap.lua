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
os.loadAPI("log")

local function init()
  local f = io.open('blocks.csv','r')
  if not f then
    log.notice("Getting blocks.csv")
    local h = rest.get("static/blocks.csv")
    
    if not h then
      log.error("Can't get blocks.csv")
    else
      local f = io.open('blocks.csv','w')
      while true do
        local chunk = h:readLine()
        
        if not chunk then break end
        
        f:write(chunk)
        f:write("\n")
      end
      f:close()
      h:close()
    end
  else
    f:close()
  end
end

init()

function toId(name)
  local f = io.open('blocks.csv','r')
  if f then
    for line in f:lines() do
      local parts = {}
      for part in line:gmatch("[^,]+") do
        table.insert(parts, part)
      end
      
      if parts[1] == name then
        return parts[2]
      end
    end
    return nil
  else
    error("toId: no blocks.csv")
  end
end


function toName(id)
  local f = io.open('blocks.csv','r')
  id = tonumber(id)
  if f then
    for line in f:lines() do
      local parts = {}
      for part in line:gmatch("[^,]+") do
        table.insert(parts, part)
      end
      
      if tonumber(parts[2]) == id then
        return parts[1]
      end
    end
    return nil
  else
    error("toName: no blocks.csv")
  end
end
