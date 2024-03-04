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
local sotnSocket = nil
local frame = 0

local function defineMemoryFunctions()
	local memDomain = {}
	local domains = memory.getmemorydomainlist()
"GPURAM"


    return domains
end

local memDomain = defineMemoryFunctions()


function receive()
    l, e = sotnSocket:receive()
    if e == 'closed' then
        if curstate == STATE_OK then
            print("Connection closed")
        end
        curstate = STATE_UNINITIALIZED
        return
    elseif e == 'timeout' then
        print("timeout")
        return
    elseif e ~= nil then
        print(e)
        curstate = STATE_UNINITIALIZED
        return
    end
    commandBlock(json.decode(l))


end

function main()
    if not checkBizHawkVersion() then
    	return
    end

    server, error = socket.bind('localhost', 52980)

    while true do
        frame = frame + 1
        if (curstate == STATE_OK) or (curstate == STATE_INITIAL_CONNECTION_MADE) or (curstate == STATE_TENTATIVELY_CONNECTED) then
            receive()
            emu.frameadvance()
        elseif (curstate == STATE_UNINITIALIZED) then
            if (frame % 60 == 0) then
                server:settimeout(2)
                print("Attempting to connect")
                local client, timeout = server:accept()
                    if (timeout == nil) then
                        print('Initial Connection Made')
                        curstate = STATE_INITIAL_CONNECTION_MADE
                        sotnSocket = client
                        sotnSocket:settimeout(2)
                    end
            end
        end
        emu.frameadvance()
    end
end


main()