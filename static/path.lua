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


os.loadAPI("log")
os.loadAPI("m")

function pathAlong(points)
  local first = table.remove(points, 1)
  if m.x() ~= first[1] or m.y() ~= first[2] or m.z() ~= first[3] then
    log.error("I am not where I am supposed to be. Should be at "..v[1]..","..v[2]..","..v[3].." but am at "..m.x..","..m.y..","..m.z)
    return false
  end
  for k,v in pairs(points) do
    -- What direction must I go? Assume these are linear
    local facing = nil
    local move = 0
    local r = 0
    -- log.debug("Move to "..v[1]..","..v[2]..","..v[3].." from "..m.x()..","..m.y()..","..m.z())
    if v[2] > m.y() then
      r=m.up(v[2]-m.y())
    elseif v[2] < m.y() then
      r=m.down(m.y()-v[2])
    elseif v[1] > m.x() then
      facing = 2
      move = v[1] - m.x()
    elseif v[1] < m.x() then
      facing = 4
      move = m.x() - v[1]
    elseif v[3] > m.z() then
      facing = 1
      move = v[3] - m.z()
    elseif v[3] < m.z() then
      facing = 3
      move = m.z() - v[3]
    end
    
    -- TODO: Optimize movement
    if facing then
      if (m.facing()%4)+1 == facing then
        m.right()
      else while facing ~= m.facing() do
          log.debug("Now: "..tostring(m.facing()).." wants: "..tostring(facing))
          m.left()
        end
      end
    end
    
    if move ~= 0 then
      r = m.forward(move)
    end
    if r ~= m.OK then
      return r
    end
    
    if m.x() ~= v[1] or m.y() ~= v[2] or m.z() ~= v[3] then
      log.error("I am not where I am supposed to be. Should be at "..v[1]..","..v[2]..","..v[3].." but am at "..m.x()..","..m.y()..","..m.z())
      return m.FAIL_UNKNOWN
    end
  end
  return m.OK
end

function findPath(x,y,z)
  return rest.api.pathing.query(m.x(), m.y(), m.z(), x, y, z)
end

function test()
  m.load()
  dest = {
    x=-18, --281-263
    y=4, --73-77
    z=-166 --308-474
  }
  
  while m.x() ~= dest.x or m.y() ~= dest.y or m.z() ~= dest.z do
    log.debug("Trying to path")
    local h = findPath(dest.x, dest.y, dest.z)
    
    log.debug("Result was "..tostring(pathAlong(h)))
  end
end