
local actions = {}
local actionNames = {}

local function init()
  local listing = fs.list("")
  
  for _, name in ipairs(listing) do
    local match = name:match("action_(.*)$")
    
    if match then
      local env = {}
      setmetatable(env, {
        __index=_G
      })
      
      local action, err = loadfile(name, env)
      
      if action then
        local ok, err = pcall(action)
        if ok then
          if env.invoke then
            actions[match] = env.invoke
            for k, v in pairs(env) do
              print(k)
            end
            table.insert(actionNames, match)
          else
            log.warning("Action '"..match.."' has no invoke!")
          end
        else
          log.error("Failed to load action '"..match.."':")
          log.error(err)
        end
      else
        log.error("Failed to read action '"..match.."':")
        log.error(err)
      end
    end
  end
end

-- List function to get list of actions
function getActions()
  return actionNames
end

-- Invoke action method, accepts data for it
function invoke(action, data)
  if actions[action] then
    local ok, err = pcall(actions[action], data)
    
    if ok then
      return err
    else
      log.error("Error trying to invoke action '"..action.."':")
      log.error(err)
      return false
    end
  else
    log.error("No such action: "..action)
    return false
  end
end

init()
