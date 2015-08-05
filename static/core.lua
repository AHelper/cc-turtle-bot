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


-- System works like this:
-- Sleep for a random amount of time
-- Call the getAction REST call
-- Pass control to whatever handler is made for this
--   Make calls for any statuses and whatnot
-- Send either a success or failure for the action
-- Loop

os.loadAPI("log")
os.loadAPI("config")
os.loadAPI("rest")
os.loadAPI("m")
os.loadAPI("actions")

log.debug("cc-turtle-bot  Copyright (C) 2015 Collin Eggert\nThis program comes with ABSOLUTELY NO WARRANTY; This is free software, and you are welcome to redistribute it under certain conditions.")
log.debug(config.id)

-- Are we new?
os.sleep(1)
local h1 = rest.api.turtle.status(config.id)

if h1 == nil then
  -- This is a new turtle!
  log.info("Attempting to register new turtle")
  local h2 = rest.api.turtle.register(config.id, 0, 0, 0, 0)
  
  if h2 then
    log.info("New turtle "..config.id.." registered")
    m.save()
  else
    log.critical("Can't make new turtle!")
  end
else
  -- Load pos from file
  m.load()
  -- Get pos from server
  local h2 = rest.api.turtle.position(config.id)
  
  if h2 ~= nil then    
    if h2.x ~= m.x() or h2.y ~= m.y() or h2.z ~= m.z() or h2.facing ~= m.facing() then
      log.notice("Our position is newer than the server's")
      h2 = rest.api.turtle.position(config.id, m.x(), m.y(), m.z(), m.facing())
    end
  else
    log.error("Failed to get position")
  end
end

-- actions.invoke("explore", {steps=100})
-- actions.invoke("move",{x=0,y=0,z=0,tries=100})

log.debug("Done!")
os.sleep(10)