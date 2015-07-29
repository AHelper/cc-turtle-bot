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

