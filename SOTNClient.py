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

CONNECTION_TIMING_OUT_STATUS = "Connection timing out. Please restart your emulator, then restart connector_sotn.lua"
CONNECTION_REFUSED_STATUS = "Connection Refused. Please start your emulator and make sure connector_sotn.lua is running"
CONNECTION_RESET_STATUS = "Connection was reset. Please restart your emulator, then restart connector_sotn.lua"
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
        self.ps1_streams: (StreamReader, StreamWriter) = None
        self.awaiting_rom = False
        self.location_table = {}
        self.messages = {}
        self.collectible_table = {}
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


def get_payload(ctx: SOTNContext):
    current_time = time.time()
    return json.dumps(
        {
            "items": [item.item for item in ctx.items_received],
            "messages": {f'{key[0]}:{key[1]}': value for key, value in ctx.messages.items()
                         if key[0] > current_time - 10}
        }
    )


async def ps1_sync_task(ctx: SOTNContext):
    logger.info("Starting ps1 connector. Use /ps1 for status information")
    while not ctx.exit_event.is_set():
        error_status = None
        if ctx.ps1_streams:
            (reader, writer) = ctx.ps1_streams
            msg = get_payload(ctx).encode()
            writer.write(msg)
            writer.write(b'\n')
            try:
                await asyncio.wait_for(writer.drain(), timeout=1.5)
                try:
                    # Data will return a dict with up to two fields:
                    # 1. A keepalive response of the Players Name (always)
                    # 2. An array representing the memory values of the locations area (if in game)
                    data = await asyncio.wait_for(reader.readline(), timeout=5)
                except asyncio.TimeoutError:
                    logger.debug("Read Timed Out, Reconnecting")
                    error_status = CONNECTION_TIMING_OUT_STATUS
                    writer.close()
                    ctx.ps1_streams = None
                except ConnectionResetError as e:
                    logger.debug("Read failed due to Connection Lost, Reconnecting")
                    error_status = CONNECTION_RESET_STATUS
                    writer.close()
                    ctx.ps1_streams = None
            except TimeoutError:
                logger.debug("Connection Timed Out, Reconnecting")
                error_status = CONNECTION_TIMING_OUT_STATUS
                writer.close()
                ctx.ps1_streams = None
            except ConnectionResetError:
                logger.debug("Connection Lost, Reconnecting")
                error_status = CONNECTION_RESET_STATUS
                writer.close()
                ctx.ps1_streams = None
            if ctx.ps1_status == CONNECTION_TENTATIVE_STATUS:
                if not error_status:
                    logger.info("Successfully Connected to ps1")
                    ctx.ps1_status = CONNECTION_CONNECTED_STATUS
                else:
                    ctx.ps1_status = f"Was tentatively connected but error occured: {error_status}"
            elif error_status:
                ctx.ps1_status = error_status
                logger.info("Lost connection to ps1 and attempting to reconnect. Use /ps1 for status updates")
        else:
            try:
                logger.debug("Attempting to connect to ps1")
                ctx.ps1_streams = await asyncio.wait_for(asyncio.open_connection("localhost", 52980), timeout=10)
                ctx.ps1_status = CONNECTION_TENTATIVE_STATUS
            except TimeoutError:
                logger.debug("Connection Timed Out, Trying Again")
                ctx.ps1_status = CONNECTION_TIMING_OUT_STATUS
                continue
            except ConnectionRefusedError:
                logger.debug("Connection Refused, Trying Again")
                ctx.ps1_status = CONNECTION_REFUSED_STATUS
                continue




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
        ctx.ps1_sync_task = asyncio.create_task(ps1_sync_task(ctx), name="PS1 Sync")

        await ctx.exit_event.wait()

        ctx.server_address = None

        await ctx.shutdown()

        if ctx.ps1_sync_task:
            await ctx.ps1_sync_task

    import colorama

    colorama.init()

    asyncio.run(main())
    colorama.deinit()
