os.loadAPI("rest")

x = 0
y = 0
z = 0
facing = 

OK = 0
BLOCK = 1
MOB = 2

UP = 0
DOWN = 1
FORWARD = 2
BACK = 3
LEFT = 4
RIGHT = 5

local moveBlock = []

function save()
  f=io.open('m_cache','w')
  f:write(textutils.serialize({
    x=x,y=y,z=z,facing=facing
  })
  f:close()
end

function load()
  f=io.open('m_cache','r')
  t=textutils.deserialize(f:readAll())
  f:close()
  x=t.x
  y=t.y
  z=t.z
  facing=t.facing
end

function sendPos()
  r=rest.post("turtle/"..config.id.."/setPosition",{
    x=x,y=y,z=z,facing=facing
  })
  if r ~= nil then
    r:close()
  end
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
  if facing == 0 then
    return x, y, z + v
  else if facing == 1 then
    return x + v, y, z
  else if facing == 2 then
    return x, y, z - v
  else if facing == 3 then
    return x - v, y, z
  else
    log.error("getLinearMovementPos: bad facing " .. tostring(facing))
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
  while times ~= 0 then
    ret = _up()
    if ret == OK then
      y = y + 1
      save()
      send()
      -- TODO: Add to movement list
    else if ret == BLOCK then
      local s,d = turtle.inspectUp()
      if s then
        sendBlock(x,y+1,z,d.name)
      end
      return BLOCK
    else if ret == MOB then
      sendObsticle(x,y+1,z)
      return MOB
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
  while times ~= 0 then
    ret = _down()
    if ret == OK then
      y = y - 1
      save()
      send()
      -- TODO: Add to movement list
    else if ret == BLOCK then
      local s,d = turtle.inspectDown()
      if s then
        sendBlock(x,y-1,z,d.name)
      end
      return BLOCK
    else if ret == MOB then
      sendObsticle(x,y-1,z)
      return MOB
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
  while times ~= 0 then
    ret = _forward()
    if ret == OK then
      x, y, z = getLinearMovementPos(1)
      save()
      send()
      -- TODO: Add to movement list
    else if ret == BLOCK then
      local s,d = turtle.inspect()
      if s then
        local a, b, c = getLinearMovementPos(1)
        sendBlock(a,b,c,d.name)
      end
      return BLOCK
    else if ret == MOB then
      local a,b,c = getLinearMovementPos(1)
      sendObsticle(a,b,c)
      return MOB
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
  while times ~= 0 then
    ret = _back()
    if ret == OK then
      x, y, z = getLinearMovementPos(-1)
      save()
      send()
      -- TODO: Add to movement list
    else if ret == BLOCK then
      local s,d = turtle.inspectDown()
      if s then
        local a, b, c = getLinearMovementPos(-1)
        sendBlock(a,b,c,d.name)
      end
      return BLOCK
    else if ret == MOB then
      local a, b, c = getLinearMovementPos(-1)
      sendObsticle(a,b,c)
      return MOB
    end
    times = times - 1
  end
end

-- Inv: inventory slot to use. If nil, use current
function place(inv)
  log.error("place: unimplemented")
  return false
end

-- Turns on the turtle in front
function on()
  log.error("on: unimplemented")
  return false
end

-- Finds the inventory number that has the block by name
function find(name)
  -- turtle.getItemDetail returns {name=,count=,metadata=}
  for 
end