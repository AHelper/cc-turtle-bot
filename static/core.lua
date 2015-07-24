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

log.debug("Core")
log.debug(config.id)

-- Are we new?
os.sleep(1)
h1 = rest.get("turtle/" .. config.id .. "/status")

if h1 == nil then
  -- This is a new turtle!
  log.info("Attempting to register new turtle")
  h2 = rest.post("turtle/"..config.id.."/register",
    {
      x=0,
      y=0,
      z=0,
      facing=0
    })
  if h2 ~= nil then
    log.info("New turtle "..config.id.." registered")
    h2:close()
  else
    log.critical("Can't make new turtle!")
  end
else
  -- Load pos from file
  m.load()
  -- Get pos from server
  h2 = rest.get("turtle/"..config.id.."/position")
  
  if h2 ~= nil then
    j = textutils.unserialize(h2:readAll())
    h2:close()
    
    if j.x ~= m.x or j.y ~= m.y or j.z ~= m.z or j.facing ~= m.facing then
      log.notice("Our position is newer than the server's")
      h2 = rest.post("turtle/"..config.id.."/position", {
        x=m.x,
        y=m.y,
        z=m.z,
        facing=m.facing
      })
      h2:close()
    end
  else
    log.error("Failed to get position")
  end
end

log.debug("Done!")
os.sleep(10)