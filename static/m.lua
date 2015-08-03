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
os.loadAPI("blockmap")

local _x = 0
local _y = 0
local _z = 0
local _facing = 1

OK = 0
BLOCK = 1
MOB = 2

UP = 0
DOWN = 1
FORWARD = 2
BACK = 3
LEFT = 4
RIGHT = 5

local useError = false

local function sendPos()
  local r=rest.post("turtle/"..config.id.."/position",{
    x=_x,y=_y,z=_z,facing=_facing
  })
  if r ~= nil then
    r:close()
  else
    log.error("sendPos: Failed to setPosition")
  end
end

function x()
  return _x
end

function y()
  return _y
end

function z()
  return _z
end

function facing()
  return _facing
end

function save()
  local f=io.open('m_cache','w')
  f:write(textutils.serialize({
    x=_x,y=_y,z=_z,facing=_facing
  }))
  f:close()
end

function load()
  local f=io.open('m_cache','r')
  local ok = false
  if f then
    local e,s = pcall(function()
      local r=f:read('*a')
      local t=textutils.unserialize(r)
      f:close()
      _x=t.x
      _y=t.y
      _z=t.z
      _facing=t.facing
    end)
    if e then
      ok = true
    end
  end
  if ok then
    sendPos()
  else
    log.error("m_cache is invalid, I am lost :(")
    error("Lost")
    -- TODO: Have it say that it is lost.  If another turtle can find it, it can verify the location. Else, disable until found
  end
end

function setError(err)
  useError = err
end

function sendBlock(x,y,z,b)
  local r=rest.post("pathing/set",{
    x=x,
    y=y,
    z=z,
    value=b
  })
  if r ~= nil then
    r:close()
  else
    log.error("sendBlock failed")
  end
end

function sendObsticle(x,y,z)
  local r=rest.post("pathing/setObsticle",{
    x=x,
    y=y,
    z=z
  })
  if r ~= nil then
    r:close()
  else
    log.error("sendObsticle failed")
  end
end

local function getLinearMovementPos(v)
  if _facing == 1 then
    return _x, _y, _z + v
  elseif _facing == 2 then
    return _x + v, _y, _z
  elseif _facing == 3 then
    return _x, _y, _z - v
  elseif _facing == 4 then
    return _x - v, _y, _z
  else
    log.error("getLinearMovementPos: bad facing " .. tostring(_facing))
  end
end

local function _up()
  if turtle.detectUp() then
    return BLOCK
  else
    if not turtle.up() then
      if turtle.detectUp() then
        return BLOCK
      else
        return MOB
      end
    else
      return OK
    end
  end
end

function up(times)
  if times == nil then
    local times = 1
  end
  while times ~= 0 do
    local ret = _up()
    if ret == OK then
      _y = _y + 1
      save()
      sendPos()
    elseif ret == BLOCK then
      local s,d = turtle.inspectUp()
      if s then
        sendBlock(_x,_y+1,_z,blockmap.toId(d.name))
      end
      if useError then
        error("up:BLOCK")
        return BLOCK
      end
    elseif ret == MOB then
      sendObsticle(_x,_y+1,_z)
      if useError then
        error("up:MOB")
      else
        return MOB
      end
    end
    times = times - 1
  end
  return OK
end

local function _down()
  if turtle.detectDown() then
    return BLOCK
  else
    if not turtle.down() then
      if turtle.detectDown() then
        return BLOCK
      else
        return MOB
      end
    else
      return OK
    end
  end
end

function down(times)
  if times == nil then
    local times = 1
  end
  while times ~= 0 do
    local ret = _down()
    if ret == OK then
      _y = _y - 1
      save()
      sendPos()
    elseif ret == BLOCK then
      local s,d = turtle.inspectDown()
      if s then
        sendBlock(_x,_y-1,_z,blockmap.toId(d.name))
      end
      if useError then
        error("down:BLOCK")
      else
        return BLOCK
      end
    elseif ret == MOB then
      sendObsticle(_x,_y-1,_z)
      if useError then
        error("down:MOB")
      else
        return MOB
      end
    end
    times = times - 1
  end
  return OK
end

local function _forward()
  if turtle.detect() then
    return BLOCK
  else
    if not turtle.forward() then
      if turtle.detect() then
        return BLOCK
      else
        return MOB
      end
    else
      return OK
    end
  end
end

function forward(times)
  if times == nil then
    local times = 1
  end
  while times ~= 0 do
    local ret = _forward()
    if ret == OK then
      _x, _y, _z = getLinearMovementPos(1)
      save()
      sendPos()
    elseif ret == BLOCK then
      local s,d = turtle.inspect()
      if s then
        local a, b, c = getLinearMovementPos(1)
        sendBlock(a,b,c,blockmap.toId(d.name))
      end
      if useError then
        error("forward:BLOCK")
      else
        return BLOCK
      end
    elseif ret == MOB then
      local a,b,c = getLinearMovementPos(1)
      sendObsticle(a,b,c)
      if useError then
        error("forward:MOB")
      else
        return MOB
      end
    end
    times = times - 1
  end
  return OK
end

-- Here's where things get interesting
local function _back()
  if turtle.back() then
    return OK
  else
    turtle.turnLeft()
    turtle.turnLeft()
    local ret = _forward()
    turtle.turnRight()
    turtle.turnRight()
    return ret
  end
end

function back(times)
  if times == nil then
    local times = 1
  end
  while times ~= 0 do
    local ret = _back()
    if ret == OK then
      _x, _y, _z = getLinearMovementPos(-1)
      save()
      sendPos()
    elseif ret == BLOCK then
      local s,d = turtle.inspectDown()
      if s then
        local a, b, c = getLinearMovementPos(-1)
        sendBlock(a,b,c,blockmap.toId(d.name))
      end
      if useError then
        error("back:BLOCK")
      else
        return BLOCK
      end
    elseif ret == MOB then
      local a, b, c = getLinearMovementPos(-1)
      sendObsticle(a,b,c)
      if useError then
        error("back:MOB")
      else
        return MOB
      end
    end
    times = times - 1
  end
  return OK
end

function left()
  turtle.turnLeft()
  if _facing ~= 1 then
    _facing = _facing - 1
  else
    _facing = 4
  end
  save()
  sendPos()
end

function right()
  turtle.turnRight()
  if _facing ~= 4 then
    _facing = _facing + 1
  else
    _facing = 1
  end
  save()
  sendPos()
end

-- Inv: inventory slot to use. If nil, use current
function place(inv)
  log.error("place: unimplemented")
  if useError then
    error("place:UNIMP")
  else
    return false
  end
end

-- Turns on the turtle in front
function on()
  log.error("on: unimplemented")
  if useError then
    error("on:UNIMP")
  else
    return false
  end
end

-- Finds the inventory number that has the block by id
function find(id)
  -- turtle.getItemDetail returns {name=,count=,metadata=}
  local pos = turtle.getSelectedSlot()
  for i=1,16,1 do
    local info = turtle.getItemDetail(i)
    if blockmap.toId(info.name) == id then
      turtle.select(pos)
      return i
    end
  end
  if useError then
    error("find:404")
  else
    return nil
  end
end

function inspect()
  local ok, data = turtle.inspect()
  local x, y, z = getLinearMovementPos(1)
  
  if ok then
    local id = blockmap.toId(data.name)
    
    rest.api.pathing.set(x, y, z, id)
    return data
  else    
    rest.api.pathing.set(x, y, z, 0)
    return nil
  end
end

function inspectUp()
  local ok, data = turtle.inspectUp()
  
  if ok then
    local id = blockmap.toId(data.name)
    
    rest.api.pathing.set(_x, _y + 1, _z, id)
    return data
  else    
    rest.api.pathing.set(_x, _y + 1, _z, 0)
    return nil
  end
end

function inspectDown()
  local ok, data = turtle.inspectDown()
  
  if ok then
    local id = blockmap.toId(data.name)
    
    rest.api.pathing.set(_x, _y - 1, _z, id)
    return data
  else    
    rest.api.pathing.set(_x, _y - 1, _z, 0)
    return nil
  end
end

function dig()
  local ok = turtle.dig()
  inspect()
  return ok
end

function digUp()
  local ok = turtle.digUp()
  inspectUp()
  return ok
end

function digDown()
  local ok = turtle.digDown()
  inspectDown()
  return ok
end
