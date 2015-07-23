os.loadAPI("rest")

local function sendLogMessage(msg, level)
  rest.post("logging/"..id.."/"..level,msg)
end

function debug(msg)
  sendLogMessage(msg,"DEBUG")
end

function error(msg)
  sendLogMessage(msg,"ERROR")
end

function notice(msg)
  sendLogMessage(msg,"NOTICE")
end

function fatal(msg)
  sendLogMessage(msg,"FATAL")
end

