# Setup
by Nikolai


## ROM

As you know, Castlevania: Symphony of the Night (SOTN) is not part of the public domain. You MUST acquire a legal copy 
of the ROM on your own. 

## Generation

You will need a valid YAML file to generate any Archipelago world. SOTN is pretty straight forward so far, so the
template will be within this documentation folder. 


## Emulation

All of this was developed for Bizhawk 2.9.1, and you will additionally need playstation core Nymashock to play. Bizhawk
does not come with the said firmware, so you will have to find it. Octoshock might work, but it is untested.


## Connecting

Load your rom, and begin a new game file. When you hear the prologue music begin, you can then open the SOTNClient, and
then you can open the Lua console, go to data/lua/connector_sotn.lua and run it. You should be connected and good to play!


### Reconnecting
Should you need to set this up again mid-game, the rule of thumb is to open the client and lua scripts after you can control Alucard


## Caution

If you have save data other than a new game for this, do not load into it. This will tell AP that you checked things that you did not check.
Nothing will be broken other than that AP experience, so you can just regenerate another seed.

# Enjoy