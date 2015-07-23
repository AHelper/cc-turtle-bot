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

id = os.getComputerID()

print("Core")
print(id)

-- Are we new?
os.sleep(1)
h1 = rest.get("turtle/" .. id .. "/status")

if h1 == nil then
  -- This is a new turtle!
  log.debug("Attempting to register new turtle")
  h2 = rest.post("turtle/"..id.."/register",
    {
      x=0,
      y=0,
      z=0,
      facing=0
    })
  if h2 ~= nil then
    log.info("New turtle "..id.." registered")
    h2:close()
  end
  else
  -- Load pos from file
  m.loadPos()
  -- Get pos from server
  h2 = rest.get("turtle/"..id.."/getPosition")
  
  if h2 ~= nil then
    j = textutils.deserialize(h2:readAll())
    h2:close()
    
    if j.x ~= m.x or j.y ~= m.y or j.z ~= m.z or j.facing ~= m.facing then
      log.notice("Our position is newer than the server's")
      h2 = rest.post("turtle/"..id.."/setPosition", {
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