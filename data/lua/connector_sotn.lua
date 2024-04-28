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
local on_drac = false


local items_by_id =  {
    "Soul of Bat" = {"relic", 620900},
    "Echo of Bat" = {"relic", 620902},
    "Soul of Wolf" = {"relic", 620904},
    "Skill of Wolf" = {"relic", 620906},
    "Power of Wolf" = {"relic", 620905},
    "Form of Mist" = {"relic", 620907},
    "Power of Mist" = {"relic", 620908},
    "Gravity Boots" = {"relic", 620912},
    "Leap Stone" = {"relic", 620913},
    "Jewel of Open" = {"relic", 620916},
    "Merman Statue" = {"relic", 620917},
    "Demon Card" =  {"relic", 620921},
    "Heart of Vlad" = {"relic", 620923},
    "Tooth of Vlad" = {"relic", 620924},
    "Rib of Vlad" = {"relic", 620925},
    "Ring of Vlad" = {"relic", 620926},
    "Eye of Vlad" = {"relic", 620927},
    "Holy Glasses" = {"item", 621141},
    "Spike Breaker" = {"item", 621121},
    "Gold Ring" = {"item", 621179},
    "Silver Ring" = {"item", 621180},
    "Bat Card" = {"relic", 620918},
    "Ghost Card" = {"relic", 620919},
    "Faerie Card" = {"relic", 620920},
    "Sword Card" = {"relic", 620922},
    "Faerie Scroll" = {"relic", 620915},
    "Cube of Zoe" = {"relic", 620910},
    "Spirit Orb" = {"relic", 620911},
    "Fire of Bat" = {"relic", 620901},
    "Force of Echo" = {"relic", 620903},
    "Gas Cloud" = {"relic", 620909},
    "Holy Symbol" = {"relic", 620914},
    "Life Max Up" = {"filler", 621476},
    "Alucard Mail" = {"item", 621122},
    "Dragon Helment" = {"item", 621152},
    "Twilight Cloak" = {"item", 621163},
    "Alucard Sword" = {"item", 621061},
    "Alucard Shield"  = {"item", 620954},
    "Walk Armor" = {"item", 621126}
}



local bosses = { -- only unchecked locations. once checked, remove from this list. List refills upon Lua script reboot
    -- ram address to AP location correlation list (vlad boss drops get 2 numbers)
    [0x03CA74] = {140014, 140015}, --Death Wing's Lair: Akmodan
    [0x03CA48] = {140004}, --Necromancy Lab: Beelzebub
    [0x03CA5C] = {136027}, --Abandoned Mine: Cerebos
    [0x03CA78] = {140005, 140007}, --Darkwing Bat
    [0x03CA58] = {140009, 140010}, --Death
    [0x03CA30] = {135010}, --Dopple10
    [0x03CA70] = {140008}, --Dopple40
    [0x03CA54] = {140006}, --Trevor and Fake Cast
    [0x03CA7C] = {140011}, --Galamoth
    [0x03CA34] = {136028}, --Granfaloon
    [0x03CA44] = {135018}, --Hippogryph
    [0x03CA50] = {135017}, --Karasuman
    [0x03CA6C] = {135015}, --Lesser Demon
    [0x03CA64] = {140003, 140002}, --Medusa
    [0x03CA38] = {136034}, --Minotaur
    [0x03CA2C] = {135030}, --Olrox
    [0x03CA3C] = {135024}, --Scylla
    [0x03CA40] = {135004}, -- Slogra and Gaibon
    [0x03CA4C] = {135023}, --Succubus
    [0x03CA68] = {140000, 140001},  --The Creature
    [0x13798C] = {135001} --Prologue Dracula
}

local cutscene_triggers = { --again, only unchecked
    -- check requires zone, room, and x value. AP item ID is last
    "Die monster You don\'t belong in this world" = {6300, 8292, 703, 135000},
    "Lost equipment" {0x187c, 15062, 54},
    "Meet Maria" = {0x37B8, 10284, 70, 135007},
    "Talk to Shopkeeper" = {0xf160, 12004, 255, 135011},
    "Post Boss Maria" = {0x5fb8, 9092, 0, 135019},
    "Maria behind doors" = {0x5fb8, 9052, 510, 135027},
    "Maria asks about Richter" = {0x9504, 10040, 254, 135013},
    "Saved Richter" = {0xd660, 7052, 320, 847, 135022},
}

local relic_locations = { --unchecked
    --techinically not all relics, but semantics
    --room, x, y, AP item ID
    "Gas Cloud" = {9360, 121, 191, 140012},
    "Force of Echo" = {11372, 114, 167, 140013},
    "Faerie Card" = {12028, 49, 167, 136014},
    "Faerie Scroll" = {12044, 1678, 167, 136013},
    "Soul of Bat" = {11972, 1060, 919, 135016},
    "Soul of Wolf" = {13556, 390, 807, 135014},
    "Fire of Bat" = {9120, 201, 183, 135037},
    "Ghost Card" = {7060, 351, 663, 136031},
    "Power of Mist" = {7052, 414, 1207, 135021},
    "Leap Stone" = {7052, 414, 1815, 135020},
    "Silver Ring" = {9052, 182, 151, 135028},
    "Sword Card" = {13076, 365, 135, 135031},
    "Echo of Bat" = {13068, 129, 135, 136030},
    "Gravity Boots" = {103, 1167, 167, 135009},
    "Form of Mist" = {11920, 237, 135, 135033},
    "Bat Card" = {10032, 117, 167, 135006},
    "Skill of Wolf" = {10096, 118, 167, 135036},
    "Cube of Zoe" = {15096, 272, 135, 135003},
    "Power of Wolf" = {14976, 272, 183, 135032},
    "Merman Statue" = {12700, 97, 167, 135025},
    "Holy Symbol" = {12636, 142, 167, 135026},
    "Gold Ring" = {12828, 176, 167, 135034},
    "Spirit Orb" = {10228, 130, 996, 135008},
    "Spike Breaker" = {11212, 47, 135, 135029},
    "Demon Card" = {6584, 90, 167, 135012},

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


local function give_relic(address_of_relic)
    memDomain.saveram()
    memory.writebyte(address_of_relic, 3)
end

local function deny_relic(address)
    --player will be grabbing vanilla relics, deny them the relic if AP deemed they haven't earned it yet
    memDomain.saveram()
    memory.writebyte(address, 0)
end

local function give_item(address_of_item)
    memDomain.saveram()
    memory.writebyte(address_of_item, memory.read_u8_le(address_of_item) + 1) -- add 1 to inventory

end


local function remove_item_from_inventory(address_of_item)
    memDomain.saveram()
    memory.writebyte(address_of_item, 0)
end

local function check_bosses(current_checks)

    for key, value in pairs(bosses) do --for every unchecked boss, check if I killed them
        if memory.read_u8_le(key) != 0
            for index, item_id in pairs(value) do --some addresses have multiple items for the check, so get them all
                table.insert(current_checks, item_id) -- distribute AP Item
                table.remove(bosses, key) -- boss is dead, so no need to check anymore
            end
        end
    end
    return current_checks
end


local function check_relics(current_checks)
    local x_position = memory.read_u32_le(0x0973F0)
    local y_position = memory.read_u32_le(0x0973F4)
    local position_tolerance = 15 --don't be pixel perfect since the relics themselves have multi-pixel hitboxes

    local room = memory.read_u32_le(0x1375BC)

    for relic, info in relic_locations do
        if room == info[1] and math.abs(x_position - info[2]) < position_tolerance and math.abs(y_position - info[3]) then
            table.insert(current_checks, info[4]) --append AP ID to send back
            table.remove(relic_locations, relic) -- reduce the size of not found relics
        end
    end
    return current_checks
end


local function check_cutscenes(current_checks)
    local x_position = memory.read_u32_le(0x0973F0)
    local position_tolerance = 15

    local room = memory.read_u32_le(0x1375BC)

    for cutscene, info in cutscene_triggers do
        if room == info[1] and math.abs(x_position - info[2]) < position_tolerance then
            table.insert(current_checks, info[3]) --grab AP item ID to send back
            table.remove(cutscene_triggers, cutscene) -- clear out checks
        end
    end
    return current_checks
end


local function check_victory() --
    local room = memory.read_u32_le(0x1375BC)
    local drac_hp = memory.read_u16_le(0x076ed6)

    if room != 5236 then -- special room for final fight
        on_drac = false
        return false
    end
    if on_drac == false and drac_hp == 10000 then
        on_drac = true
        return false
    end
    if drac_hp > 20000 or drac_hp == 0 then
        return true
    end
    return false
end

function receive(already_checked)
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
    total_checks = check_bosses(already_checked)
    total_checks = check_cutscenes(total_checks)
    total_checks = check_relics()
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
    checked_locations = {}
    while true do
        frame = frame + 1
        if (curstate == STATE_OK) or (curstate == STATE_INITIAL_CONNECTION_MADE) or (curstate == STATE_TENTATIVELY_CONNECTED) then
            checked_locations = receive()
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