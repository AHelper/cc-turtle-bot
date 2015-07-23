os.loadAPI("rest")

local function sendLogMessage(msg, level)
  rest.post("logging/"..id.."/"..level,msg)
  print("["..level..
end

function debug(msg)
  sendLogMessage(msg,7,"DEBUG")
end

function error(msg)
  sendLogMessage(msg,3,"ERROR")
end

function notice(msg)
  sendLogMessage(msg,5,"NOTICE")
end

function critical(msg)
  sendLogMessage(msg,2,"CRITICAL")
end

