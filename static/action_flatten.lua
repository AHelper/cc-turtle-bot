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


os.loadAPI("m")

-- ACTION: Flattens a plot to a certain Y value using a certain block and clears the area above
-- data:
--   x: INT
--   y: INT
--   z: INT
--   height: INT
--   floor: INT
--   block: INT

-- Keep trying to path to the center of the to-be empty region
-- Once inside, dig to the local 0,0 corner, then down to the floor.
-- Clear the empty region layer by layer
-- Go back to the floor
-- For every space, go down until a block is hit, then fill back up.
