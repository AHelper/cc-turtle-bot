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
-- Distance to go down before calling it a hole and getting out
local HOLE_DEPTH = 2
-- Distance to go up to see if it wraps over to call it a ceiling
local CEILING_HEIGHT = 10

local function detectHole()
  
end

local function detectCeiling()
  
end

function invoke(data)
  
end