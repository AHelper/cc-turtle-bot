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
