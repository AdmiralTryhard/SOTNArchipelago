local socket = require("socket")
local json = require('json')
local math = require('math')
require("common")


local STATE_OK = "Ok"
local STATE_TENTATIVELY_CONNECTED = "Tentatively Connected"
local STATE_INITIAL_CONNECTION_MADE = "Initial Connection Made"
local STATE_UNINITIALIZED = "Uninitialized"


local consumableStacks = nil
local prevstate = ""
local curstate =  STATE_UNINITIALIZED
local ff1Socket = nil
local frame = 0



function main()
    if not checkBizHawkVersion then
    	return
    end

    server, error = socket.bind('localhost', 52980)

    while true do
        frame = frame + 1
        if not (curstate == prevstate) then
            -- console.log("Current state: "..curstate)
            prevstate = curstate
        end



    end
end