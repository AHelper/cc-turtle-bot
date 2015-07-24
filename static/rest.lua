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
  url = buildUrl(action)
  if get_string then
    h = http.post(url, textutils.serializeJSON(json))
    str = h:readAll()
    h:close()
    return str
  else
    return http.post(url, textutils.serializeJSON(json))
  end
end
