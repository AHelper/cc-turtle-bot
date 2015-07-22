os.loadAPI("config")

function buildUrl(action)
  return config.server..action
end

function get(action)
  url = buildUrl(action)
  return http.get(url)
end

function post(action, json)
  url = buildUrl(action)
  return http.post(url, textutils.serializeJSON(json))
end
