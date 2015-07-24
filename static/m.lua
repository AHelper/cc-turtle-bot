os.loadAPI("rest")

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
  r=rest.post("turtle/"..config.id.."/position",{
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
  f=io.open('m_cache','w')
  f:write(textutils.serialize({
    x=_x,y=_y,z=_z,facing=_facing
  }))
  f:close()
end

function load()
  f=io.open('m_cache','r')
  local ok = false
  if f then
    e,s = pcall(function()
      r=f:read('*a')
      t=textutils.unserialize(r)
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
  r=rest.post("pathing/set",{
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
  r=rest.post("pathing/setObsticle",{
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
    times = 1
  end
  while times ~= 0 do
    ret = _up()
    if ret == OK then
      _y = _y + 1
      save()
      sendPos()
    elseif ret == BLOCK then
      local s,d = turtle.inspectUp()
      if s then
        sendBlock(_x,_y+1,_z,d.name)
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

function down()
  if times == nil then
    times = 1
  end
  while times ~= 0 do
    ret = _down()
    if ret == OK then
      _y = _y - 1
      save()
      sendPos()
    elseif ret == BLOCK then
      local s,d = turtle.inspectDown()
      if s then
        sendBlock(_x,_y-1,_z,d.name)
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
    times = 1
  end
  while times ~= 0 do
    ret = _forward()
    if ret == OK then
      _x, _y, _z = getLinearMovementPos(1)
      save()
      sendPos()
    elseif ret == BLOCK then
      local s,d = turtle.inspect()
      if s then
        local a, b, c = getLinearMovementPos(1)
        sendBlock(a,b,c,d.name)
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
end

-- Here's where things get interesting
local function _back()
  if turtle.back() then
    return OK
  else
    turtle.turnLeft()
    turtle.turnLeft()
    ret = _forward()
    turtle.turnRight()
    turtle.turnRight()
    return ret
  end
end

function back(times)
  if times == nil then
    times = 1
  end
  while times ~= 0 do
    ret = _back()
    if ret == OK then
      _x, _y, _z = getLinearMovementPos(-1)
      save()
      sendPos()
    elseif ret == BLOCK then
      local s,d = turtle.inspectDown()
      if s then
        local a, b, c = getLinearMovementPos(-1)
        sendBlock(a,b,c,d.name)
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

-- Finds the inventory number that has the block by name
function find(name)
  -- turtle.getItemDetail returns {name=,count=,metadata=}
  pos = turtle.getSelectedSlot()
  for i=1,16,1 do
    info = turtle.getItemDetail(i)
    if info.name == name then
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
