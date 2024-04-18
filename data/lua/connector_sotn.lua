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


local bosses = {
    -- ram address to AP location correlation list
    [0x03CA74] = 140014, --Death Wing's Lair: Akmodan
    [0x03CA48] = 140004, --Necromancy Lab: Beelzebub
    [0x03CA5C] = 136027, --Abandoned Mine: Cerebos
    [0x03CA78] = 140005, --Darkwing Bat
    [0x03CA58] = 140009, --Death
    [0x03CA30] = 135010, --Dopple10
    [0x03CA70] = 140008, --Dopple40
    [0x03CA54] = 140006, --Trevor and Fake Cast
    [0x03CA7C] = 140011, --Galamoth
    [0x03CA34] = 136028, --Granfaloon
    [0x03CA44] = 135018, --Hippogryph
    [0x03CA50] = 135017, --Karasuman
    [0x03CA6C] = 135015, --Lesser Demon
    [0x03CA64] = 140003, --Medusa
    [0x03CA38] = 136034, --Minotaur
    [0x03CA2C] = 135030, --Olrox
    [0x03CA3C] = 135024, --Scylla
    [0x03CA40] = 135004, -- Slogra and Gaibon
    [0x03CA4C] = 135023, --Succubus
    [0x03CA68] = 140000 --The Creature
}

local function defineMemoryFunctions()
	local memDomain = {}
	local domains = memory.getmemorydomainlist()

    memDomain["systembus"] = function() memory.usememorydomain("System Bus") end
	memDomain["saveram"]   = function() memory.usememorydomain("MainRAM") end
	memDomain["rom"]       = function() memory.usememorydomain("BiosROM") end

    return memDomain
end

local memDomain = defineMemoryFunctions()

local function check_address(address)
    -- 0x097BA0 is your current health
    memDomain.saveram()
    value = memory.read_u32_le(address)
    return value

end

local function give_relic(address_of_relic)
    memDomain.saveram()
    memory.writebyte(address_of_relic, 3)
end

local function deny_relic(address)
    --temporary since I do not know the ram address of the location, just if I have one
    memDomain.saveram()
    memory.writebyte(address, 0)
end

function check_bosses()
    checked_bosses = {}
    if check_address(0x03CA40) == 827 then
        checked_bosses = 135004
    end
    -- print(checked_bosses)
    return checked_bosses
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
    local returnTable = {}
    returnTable["player"] = "SOTN"
    returnTable["locations"] = check_bosses()
    msg = json.encode(returnTable).."\n"
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
    emu.frameadvance()

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