import asyncio
import json
import os
import multiprocessing
import subprocess
import zipfile
from asyncio import StreamReader, StreamWriter

# CommonClient import first to trigger ModuleUpdater
from CommonClient import CommonContext, server_loop, gui_enabled, \
    ClientCommandProcessor, logger, get_base_parser
import Utils
from Utils import async_start
from worlds import network_data_package

CONNECTION_TIMING_OUT_STATUS = "Connection timing out. Please restart your emulator, then restart connector_ff1.lua"
CONNECTION_REFUSED_STATUS = "Connection Refused. Please start your emulator and make sure connector_ff1.lua is running"
CONNECTION_RESET_STATUS = "Connection was reset. Please restart your emulator, then restart connector_ff1.lua"
CONNECTION_TENTATIVE_STATUS = "Initial Connection Made"
CONNECTION_CONNECTED_STATUS = "Connected"
CONNECTION_INITIAL_STATUS = "Connection has not been initiated"



"""This is where the Lua hooks will be"""




if __name__ == '__main__':

    Utils.init_logging("SOTNClient")