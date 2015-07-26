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
            post("pathing/set", {
              x=x,
              y=y,
              z=z,
              value=value
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
                return textutils.unserialize(str).pathing
              else
                return nil
              end
            end
  }
}
