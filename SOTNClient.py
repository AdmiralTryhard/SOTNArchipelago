from __future__ import annotations

import copy
import logging
import asyncio
import urllib.parse
import sys
import typing
import time
import functools
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


class SOTNCommandProcessor(ClientCommandProcessor):
    def __init__(self, ctx):
        super().__init__(ctx)

    def _cmd_ps1(self):
        """Check PS1 Connection State"""
        if isinstance(self.ctx, SOTNContext):
            logger.info(f"PS1 Status: {self.ctx.ps1_status}")


class SOTNContext(CommonContext):
    command_processor = SOTNCommandProcessor
    items_handling = 0b111  # full remote
    game = "Symphony of the Night"
    def __init__(self, server_address, password):
        super().__init__(server_address, password)
        self.game = "Symphony of the Night"
        self.ps1_status = CONNECTION_INITIAL_STATUS
        self.awaiting_rom = False
        self.location_table = {}
        self.collectible_table = {}
        self.collectible_override_flags_address = 0
        self.collectible_offsets = {}


    async def server_auth(self, password_requested: bool = False):
        if password_requested and not self.password:
            await super(SOTNContext, self).server_auth(password_requested)
        if not self.auth:
            self.awaiting_rom = True
            logger.info('Waiting for connection to Emuhawk for player info')
            return
        await self.send_connect()

    def run_gui(self):
        from kvui import GameManager

        class SOTNManager(GameManager):
            log_pairs = [
                ("Client", "Archipelago")
            ]
            base_title = "Symphony of the Night Client"

        self.ui = SOTNManager(self)
        self.ui_task = asyncio.create_task(self.ui.async_run(), name="UI")

if __name__ == '__main__':
    gui_enabled = not sys.stdout or "--nogui" not in sys.argv

    Utils.init_logging("SOTNClient")

    async def main():
        multiprocessing.freeze_support()
        parser = get_base_parser()
        args = parser.parse_args()

        ctx = SOTNContext(args.connect, args.password)
        ctx.server_task = asyncio.create_task(server_loop(ctx), name="Server Loop")

        if gui_enabled:
            ctx.run_gui()
        ctx.run_cli()

        ctx.server_address = None
        await ctx.exit_event.wait()

        await ctx.shutdown()

    import colorama

    colorama.init()

    asyncio.run(main())
    colorama.deinit()
