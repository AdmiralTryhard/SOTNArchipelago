local socket = require("socket")
local json = require('json')
local math = require('math')
require("common")


local STATE_OK = "Ok"
local STATE_TENTATIVELY_CONNECTED = "Tentatively Connected"
local STATE_INITIAL_CONNECTION_MADE = "Initial Connection Made"
local STATE_UNINITIALIZED = "Uninitialized"

local prevstate = ""
local curstate =  STATE_UNINITIALIZED
local sotnSocket = nil
local frame = 0
local on_drac = false --dracula is the final boss


local already_granted_items = {
    -- same structure as items_by_id
} -- build item granted list to check if you need to deny relics


local items_by_id =  {
    -- AP item index (not location index) = type, item name, ram address_of_item
    [620900] = {"relic", "Soul of Bat", 0x097964},
    [620902] = {"relic", "Echo of Bat", 0x097966},
    [620904] = {"relic", "Soul of Wolf", 0x097968},
    [620906] = {"relic", "Skill of Wolf", 0x09796A},
    [620905] = {"relic", "Power of Wolf", 0x097969},
    [620907] = {"relic", "Form of Mist", 0x09796B},
    [620908] = {"relic", "Power of Mist", 0x09796C},
    [620912] = {"relic", "Gravity Boots", 0x097970},
    [620913] = {"relic", "Leap Stone", 0x097971},
    [620916] = {"relic", "Jewel of Open", 0x097974},
    [620917] = {"relic", "Merman Statue", 0x097975},
    [620921] = {"relic", "Demon Card", 0x097979},
    [620923] = {"relic", "Heart of Vlad", 0x09797D},
    [620924] = {"relic", "Tooth of Vlad", 0x09797E},
    [620925] = {"relic", "Rib of Vlad", 0x09797F},
    [620926] = {"relic", "Ring of Vlad", 0x097980},
    [620927] = {"relic", "Eye of Vlad", 0x097981},
    [621141] = {"item", "Holy Glasses", 0x097A55},
    [621121] = {"item", "Spike Breaker", 0x097A41},
    [621179] = {"item", "Gold Ring", 0x097A7B},
    [621180] = {"item", "Silver Ring", 0x097A7C},
    [620918] = {"relic", "Bat Card", 0x097976},
    [620919] = {"relic", "Ghost Card", 0x097977},
    [620920] = {"relic", "Faerie Card", 0x097978},
    [620922] = {"relic", "Sword Card", 0x09797A},
    [620915] = {"relic", "Faerie Scroll", 0x097973},
    [620910] = {"relic", "Cube of Zoe", 0x09796E},
    [620911] = {"relic", "Spirit Orb", 0x09796F},
    [620901] = {"relic", "Fire of Bat", 0x097965},
    [620903] = {"relic", "Force of Echo", 0x097967},
    [620909] = {"relic", "Gas Cloud", 0x09796D},
    [620914] = {"relic", "Holy Symbol", 0x097972},
    [621476] = {"filler", "Life Max Up", 0x000001},
    [621122] = {"item", "Alucard Mail", 0x097A42},
    [621152] = {"item", "Dragon Helmet", 0x097A60},
    [621163] = {"item", "Twilight Cloak", 0x097A6B},
    [621061] = {"item", "Alucard Sword", 0x097A05},
    [620954] = {"item", "Alucard Shield", 0x09799A},
    [621126] = {"item", "Walk Armor", 0x097A46}
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
}

local cutscene_triggers = { --again, only unchecked
    -- check requires room, and x value. AP item ID is last
    {8292, 158, 135000}, --die monster you don't belong
    {15648, 52, 135002}, --death taking your stuff
    {4848, 176, 135007}, --meet maria
    {12004, 255, 135011}, --see shopkeep
    {9092, 0, 135019}, -- royal chapel maria post boss
    {9052, 510, 135027}, --silver ring maria
    {10040, 254, 135013}, --alchemy lab maria
    {7052, 320, 847, 135022} -- saved richter
}

local relic_locations = { --unchecked
    --techinically not all relics, but semantics
    --room, x, y, AP location ID, AP item_id
    {9360, 121, 191, 140012, 620909}, -- Gas Cloud
    {11372, 114, 167, 140013, 620903}, -- Force of Echo
    {12028, 49, 167, 136014, 620920}, -- Faerie Card
    {12044, 1678, 167, 136013, 620915}, -- Faerie Scroll
    {11972, 1060, 919, 135016, 620900}, -- Soul of Bat
    {13556, 390, 807, 135014, 620904}, -- Soul of Wolf
    {9120, 201, 183, 135037, 620901}, -- Fire of Bat
    {7060, 351, 663, 136031, 620919}, -- Ghost Card
    {7052, 414, 1207, 135021, 620908}, -- Power of Mist
    {7052, 414, 1815, 135020, 620913}, -- Leap Stone
    {9052, 182, 151, 135028, 621180}, -- Silver Ring
    {13076, 365, 135, 135031, 620922}, -- Sword Card
    {13068, 129, 135, 136030, 620902}, -- Echo of Bat
    {103, 1167, 167, 135009, 620912}, -- Gravity Boots
    {11920, 237, 135, 135033, 620907}, -- Form of Mist
    {10032, 117, 167, 135006, 620918}, -- Bat Card
    {10096, 118, 167, 135036, 620906}, -- Skill of Wolf
    {15680, 272, 135, 135003, 620910}, -- Cube of Zoe
    {14976, 272, 183, 135032, 620905}, -- Power of Wolf
    {12700, 97, 167, 135025, 620917}, -- Merman Statue
    {12636, 142, 167, 135026, 620914}, -- Holy Symbol
    {12828, 176, 167, 135034, 621179}, -- Gold Ring
    {10228, 130, 1011, 135008, 620911}, -- Spirit Orb
    {11212, 47, 135, 135029, 621121}, -- Spike Breaker
    {6584, 90, 167, 135012, 620921} -- Demon Card
}


local function give_relic(address_of_relic)
    mainmemory.writebyte(address_of_relic, 3)
end

local function deny_relic(address)
    --player will be grabbing vanilla relics, deny them the relic if AP deemed they haven't earned it yet
    mainmemory.writebyte(address, 0)
end

local function give_item(address_of_item, count)
    mainmemory.writebyte(address_of_item, mainmemory.read_u8_le(address_of_item) + count) -- add count to inventory
end


local function raise_max_hp()
    local max_hp = mainmemory.read_u16_le(0x097BA4)
    max_hp = max_hp + 5
    mainmemory.write_u16_le(0x097BA4, max_hp)
end


local function distribute_items(message)
    local itemsBlock = message["items"]

    for _, item in pairs(itemsBlock) do --index doesn't matter, but item ID does
        if already_granted_items[item] == nil then
            local full_item = items_by_id[item]
            already_granted_items[item] = full_item --add to already added items
            if full_item[1] == "relic" then
                give_relic(full_item[3])
            elseif full_item[1] == "item" then
                give_item(full_item[3], 1)
            else
                raise_max_hp()
            end
        end
    end
end


local function check_bosses(current_checks)

    for key, value in pairs(bosses) do --for every unchecked boss, check if I killed them
        local boss_address = mainmemory.read_u32_le(key)
        if boss_address ~= 0 then
            for _, item_id in pairs(value) do --some addresses have multiple items for the check, so get them all
                if current_checks ~= nil then
                	current_checks[#current_checks+1] = item_id -- distribute AP Item
                else
                    current_checks = {item_id}
                end
            end
        end
    end
    return current_checks
end


local function check_relics(current_checks)
    local x_position = mainmemory.read_u16_le(0x0973F0)
    local y_position = mainmemory.read_u16_le(0x0973F4)
    local position_tolerance = 5 --don't be pixel perfect since the relics themselves have multi-pixel hitboxes

    local room = mainmemory.read_u16_le(0x1375BC)

    for relic, info in pairs(relic_locations) do
        if room == info[1] and math.abs(x_position - info[2]) < position_tolerance and math.abs(y_position - info[3]) then
            print("grabbed a relic!")
            if current_checks ~= nil then
                current_checks[#current_checks+1] = info[4] --append AP ID to send back
            else
                current_checks = {info[4]}
            end
            local item_id = info[5]
            if already_granted_items[item_id] == nil then
                local grabbed_relic = items_by_id[item_id]
                deny_relic(grabbed_relic[3]) -- key items and relics can just be set to 0 alike
            end
        end
    end
    return current_checks
end


local function check_cutscenes(current_checks)
    local x_position = mainmemory.read_u16_le(0x0973F0)
    local position_tolerance = 15

    local room = mainmemory.read_u16_le(0x1375BC)

    for cutscene, info in pairs(cutscene_triggers) do
        if room == info[1] and math.abs(x_position - info[2]) < position_tolerance then
            print("hey, I am in this code block")
            if current_checks ~= nil then
                current_checks[#current_checks+1] = info[3] --append AP ID to send back
            else
                current_checks = {info[3]}
            end
        end
    end
    return current_checks
end

local function check_prologue(current_checks)
    local zone = mainmemory.read_u16_le(0x180000)
    if zone ~= 6300 or mainmemory.read_u32_le(0x13798C) == 0 then
        if current_checks ~= nil then
            current_checks[#current_checks+1] = 135001
        else
            current_checks = {135001}
        end
    end
    return current_checks
end

local function check_victory() -- dracula an
    local room = mainmemory.read_u16_le(0x1375BC)
    local drac_hp = mainmemory.read_u16_le(0x076ed6)

    if room ~= 5236 then -- special room for final fight
        on_drac = false
        return false
    end
    if on_drac == false and drac_hp == 10000 then --he has a moment of flying in before you can touch him. max hp = 10000
        on_drac = true
        return false
    end
    if drac_hp > 20000 or drac_hp == 0 and on_drac then --if his hp < 0, it wraps to BIG number
        return true
    end
    return false
end

function receive()
    l, e = sotnSocket:receive()
    --check connection status
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
    -- get items
    local zone = mainmemory.read_u16_le(0x180000)
    if zone ~= 6300 then --richter doesn't get items. Not sure of how the game behaves if you give them
        distribute_items(json.decode(l))
    end
    emu.frameadvance() -- sticking this after big operations to make sure runtime isn't hurt


    -- respond
    local returnTable = {}
    returnTable["player"] = "SOTN"
    local total_checks = check_bosses({})
    emu.frameadvance()
    total_checks = check_prologue(total_checks)
    total_checks = check_cutscenes(total_checks)
    emu.frameadvance()
    total_checks = check_relics(total_checks)
    emu.frameadvance()
    if check_victory() then
        returnTable["victory"] = 'True'
    else
        returnTable["victory"] = 'False'
    end
    --print(total_checks)
    returnTable["locations"] = total_checks
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