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

    memDomain["systembus"] = function() memory.usememorydomain("System Bus") end
	memDomain["saveram"]   = function() memory.usememorydomain("MainRAM") end
	memDomain["rom"]       = function() memory.usememorydomain("BiosROM") end

    return memDomain
end

local memDomain = defineMemoryFunctions()

local function check_address()
    memDomain.saveram()
    -- This will just check a dummy address for now. Health value works since it's at 69.
    local health = memory.readbyte(0x097BA0)

    return health

end

local function give_2nd_jump()
    memDomain.saveram()
    memory.writebyte(0x97971, 3)
end


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

    -- respond
    memDomain.rom()
    local playerName = "AdmiralTryhard"
    local returnTable = {}
    msg = json.encode(retTable).."\n"
    local ret, error = sotnSocket:send(msg)
    if ret == nil then
        print(error)
    elseif curstate == STATE_INITIAL_CONNECTION_MADE then
        curstate = STATE_TENTATIVELY_CONNECTED
    elseif curstate == STATE_TENTATIVELY_CONNECTED then
        print("Connected!")
        itemMessages["(0,0)"] = {TTL=240, message="Connected", color="green"}
        curstate = STATE_OK
    end



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
        local health = check_address()
        if health > 70 then
            give_2nd_jump()
        end
        emu.frameadvance()
    end
end


main()