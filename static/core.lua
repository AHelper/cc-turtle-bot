-- System works like this:
-- Sleep for a random amount of time
-- Call the getAction REST call
-- Pass control to whatever handler is made for this
--   Make calls for any statuses and whatnot
-- Send either a success or failure for the action
-- Loop

print("Core")

print(os.getComputerID())