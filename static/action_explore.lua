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


-- ACTION: Explores the *surface*, logging what it bumps into, recording ceilings and holes.
-- data:
--   steps: INT

local OK = 0
local FOUND = 1
local NOT_FOUND = 2
-- Distance to go down before calling it a hole and getting out
local HOLE_DEPTH = 4
-- Distance to go up to see if it wraps over to call it a ceiling
local CEILING_HEIGHT = 10

-- Returns true if it is a hole, false if it found ground
-- If true, returned back up to where it was.
-- Call with no arguments
local function detectHole(depth)
  if not depth then
    depth = 0
  end
  local ok = m.inspectDown()

  if ok ~= nil then
    return NOT_FOUND
  else
    if depth+1 == HOLE_DEPTH then
      return FOUND
    else
      m.down()
      if detectHole(depth+1) == FOUND then
        m.up()
        return FOUND
      else
        return NOT_FOUND
      end
    end
  end
end

local function detectCeiling(height)
  if not height then
    height = 0
  end
  local ok = m.forward()

  if ok == m.OK then
    return OK
  end

  ok = m.up()

  if ok ~= m.OK then
    return FOUND
  else
    if height == CEILING_HEIGHT then
      ok = m.inspectUp() ~= nil
      m.down()
      if ok then
        return FOUND
      else
        return NOT_FOUND
      end
    else
      ok = detectCeiling(height+1)
      if ok ~= OK then
        m.down()
      end
      return ok
    end
  end
end

local function doTurn(turn)
  if turn == 1 then
    m.left()
    return 2
  elseif turn == 2 then
    m.left()
    return 3
  else
    m.right()
    return 1
  end
end

local function shouldTurn()
  return math.random(20) == 1
end

function invoke(data)
  -- Pick a random direction (floating)
  -- Loop:
  -- If the heading is not one of the 2 headings to go in

  local turn = 1

  -- Find the ground first
  while m.inspectDown() == nil do
    local ok = m.down()

    if ok ~= m.OK then
      log.debug("Found ground (maybe)")
      break
    end
  end

  for x=1,data.distance,1 do
    local ok = m.forward()

    if ok ~= m.OK then
      log.debug("Hit something, checking for ceiling")
      local ok = detectCeiling()
      if ok ~= OK then
        turn = doTurn(turn)
      end
    else
      local ok = m.inspectDown()

      if ok == nil then
        log.debug("Nothing below me, checking for hole")

        local ok = detectHole()

        if ok == FOUND then
          m.back()
          turn = doTurn(turn)
        end
      end
    end

    if shouldTurn() then
      turn = doTurn(turn)
    end
  end

  return true
end
