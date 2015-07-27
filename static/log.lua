os.loadAPI("rest")
os.loadAPI("config")

local function sendLogMessage(msg, level,levelstr)
  rest.post("logging/"..config.id.."/"..level,msg)
  print("["..levelstr.."] "..msg)
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

function warning(msg)
  sendLogMessage(msg,4,"WARNING")
end

function info(msg)
  notice(msg)
end

function critical(msg)
  sendLogMessage(msg,2,"CRITICAL")
end

