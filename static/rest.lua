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


os.loadAPI("config")

function buildUrl(action)
  return config.server..action
end

function get(action, get_string)
  url = buildUrl(action)
  if get_string then
    h = http.get(url)
    if h then
      str = h:readAll()
      h:close()
    end
    return str
  else
    return http.get(url)
  end
end

function post(action, json, get_string)
  local url = buildUrl(action)
  if get_string then
    local h = http.post(url, textutils.serializeJSON(json))
    if h then
      local str = h:readAll()
      h:close()
      return str
    else
      return nil
    end
  else
    return http.post(url, textutils.serializeJSON(json))
  end
end

-- Utility functions

api = {
  pathing = {
    get = function(x,y,z)
            local str = post("pathing/get", {
              x=x,
              y=y,
              z=z
            }, true)

            if str then
              return textutils.unserialize(str).value
            else
              return nil
            end
          end,
    set = function(x,y,z,value)
            return post("pathing/set", {
              x=x,
              y=y,
              z=z,
              value=value
            }, true)
          end,
    setObsticle = function(x,y,z)
                    return post("pathing/setObsticle", {
                      x=x,
                      y=y,
                      z=z
                    }, true)
                  end,
    query = function(sx,sy,sz,dx,dy,dz)
              local str = post("pathing/query", {
                source = {
                  x=sx,
                  y=sy,
                  z=sz
                },
                destination = {
                  x=dx,
                  y=dy,
                  z=dz
                }
              }, true)

              if str then
                return textutils.unserialize(str).path
              else
                return nil
              end
            end
  },
  turtle = {
    register = function(id, x, y, z, facing)
                 local str = post("turtle/"..id.."/register", {
                   x=x,
                   y=y,
                   z=z,
                   facing=facing
                 }, true)

                 if str then
                   return textutils.unserialize(str).type == "success"
                 else
                   return nil
                 end
               end,
    unregister = function(id)
                   local str = post("turtle/"..id.."/unregister", {}, true)

                   if str then
                     return textutils.unserialize(str).type == "success"
                   else
                     return nil
                   end
                 end,
    status = function(id)
               local str = get("turtle/"..id.."/status", {}, true)

               if str then
                 return textutils.unserialize(str)
               else
                 return nil
               end
             end,
    position = function(id, x, y, z, facing)
                 local str
                 if x == nil and y == nil and z == nil and facing == nil then
                   str = get("turtle/"..id.."/position", {}, true)

                   if str then
                     return textutils.unserialize(str)
                   else
                     return nil
                   end
                 else
                   str = post("turtle/"..id.."/position", {
                     x=x,
                     y=y,
                     z=z,
                     facing=facing
                   }, true)

                   if str then
                     return textutils.unserialize(str).type == "success"
                   else
                     return nil
                   end
                 end
               end,
    getAction = function(id)
                   local str = get("turtle/"..id.."/getAction", {}, true)

                   if str then
                     return textutils.unserialize(str)
                   else
                     return nil
                   end
                end,
    response = function(id, response)
                return post("turtle/"..id.."/response", response, true)
              end
  },
  logging = {
    log = function(id, level, msg)
            return post("logging/"..id.."/"..level, msg, true)
          end
  }
}
