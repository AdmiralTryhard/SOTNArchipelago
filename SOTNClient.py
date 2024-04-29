from __future__ import annotations
import copy
import sys
import typing
import time
import asyncio
import json
import multiprocessing

from asyncio import StreamReader, StreamWriter

# CommonClient import first to trigger ModuleUpdater
from CommonClient import CommonContext, server_loop, gui_enabled, \
    ClientCommandProcessor, logger, get_base_parser
import Utils
from Utils import async_start


SYSTEM_MESSAGE_ID = 0

CONNECTION_TIMING_OUT_STATUS = "Connection timing out. Please restart your emulator, then restart connector_sotn.lua"
CONNECTION_REFUSED_STATUS = "Connection Refused. Please start your emulator and make sure connector_sotn.lua is running"
CONNECTION_RESET_STATUS = "Connection was reset. Please restart your emulator, then restart connector_sotn.lua"
CONNECTION_TENTATIVE_STATUS = "Initial Connection Made"
CONNECTION_CONNECTED_STATUS = "Connected"
CONNECTION_INITIAL_STATUS = "Connection has not been initiated"

DISPLAY_MSGS = True


"""This is where the Lua hooks will be"""


class SOTNCommandProcessor(ClientCommandProcessor):
    def __init__(self, ctx):
        super().__init__(ctx)

    def _cmd_psx(self):
        """Check psx Connection State"""
        if isinstance(self.ctx, SOTNContext):
            logger.info(f"psx Status: {self.ctx.psx_status}")


class SOTNContext(CommonContext):
    command_processor = SOTNCommandProcessor
    items_handling = 0b111  # full remote
    game = "sotn"

    def __init__(self, server_address, password):
        super().__init__(server_address, password)
        self.username = None
        self.game = "sotn"
        self.psx_status = CONNECTION_INITIAL_STATUS
        self.psx_streams: (StreamReader, StreamWriter) = None
        self.psx_sync_task = None
        self.awaiting_rom = False
        self.locations_array = None
        self.messages = {}

    def _set_message(self, msg: str, msg_id: int):
        if DISPLAY_MSGS:
            self.messages[time.time(), msg_id] = msg

    def on_print_json(self, args: dict):
        if self.ui:
            self.ui.print_json(copy.deepcopy(args["data"]))
        else:
            text = self.jsontotextparser(copy.deepcopy(args["data"]))
            logger.info(text)
        relevant = args.get("type", None) in {"Hint", "ItemSend"}
        if relevant:
            item = args["item"]
            # goes to this world
            if self.slot_concerns_self(args["receiving"]):
                relevant = True
            # found in this world
            elif self.slot_concerns_self(item.player):
                relevant = True
            # not related
            else:
                relevant = False
            if relevant:
                item = args["item"]
                msg = self.raw_text_parser(copy.deepcopy(args["data"]))
                self._set_message(msg, item.item)
    async def server_auth(self, password_requested: bool = False):
        if password_requested and not self.password:
            await super(SOTNContext, self).server_auth(password_requested)
        await self.get_username()
        if not self.auth:
            self.awaiting_rom = True
            logger.info('Waiting for connection to Emuhawk for player info')
            return

        await self.send_connect()

    def on_package(self, cmd: str, args: dict):
        if cmd == 'Connected':
            async_start(parse_locations(self.locations_array, self, True))
        elif cmd == 'Print':
            msg = args['text']


    async def get_username(self):
        if not self.auth:
            self.auth = self.username
            if not self.auth:
                logger.info('Enter slot name:')
                self.auth = await self.console_input()
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
    """game reporting all of the locations it has found thus_far"""
    return json.dumps(
        {
            "items": [item.item for item in ctx.items_received]
        }
    )


async def psx_sync_task(ctx: SOTNContext):
    logger.info("Starting psx connector. Use /psx for status information")
    while not ctx.exit_event.is_set():
        error_status = None
        if ctx.psx_streams:
            (reader, writer) = ctx.psx_streams
            msg = get_payload(ctx).encode()
            writer.write(msg)
            writer.write(b'\n')
            try:
                await asyncio.wait_for(writer.drain(), timeout=1.5)
                try:
                    # Data should return a dict with up to two fields:
                    # 1. A keepalive response (always)
                    # 2. An array representing the memory values of found locations
                    data = await asyncio.wait_for(reader.readline(), timeout=5)
                    data_decoded = json.loads(data.decode())
                    if ctx.game is not None and 'locations' in data_decoded:
                        # Not just a keep alive ping, parse
                        async_start(parse_locations(data_decoded['locations'], ctx, False))
                        async_start(check_victory(data_decoded['victory'], ctx))
                except asyncio.TimeoutError:
                    logger.debug("Read Timed Out, Reconnecting")
                    error_status = CONNECTION_TIMING_OUT_STATUS
                    writer.close()
                    ctx.psx_streams = None
                except ConnectionResetError as e:
                    logger.debug("Read failed due to Connection Lost, Reconnecting")
                    error_status = CONNECTION_RESET_STATUS
                    writer.close()
                    ctx.psx_streams = None
            except TimeoutError:
                logger.debug("Connection Timed Out, Reconnecting")
                error_status = CONNECTION_TIMING_OUT_STATUS
                writer.close()
                ctx.psx_streams = None
            except ConnectionResetError:
                logger.debug("Connection Lost, Reconnecting")
                error_status = CONNECTION_RESET_STATUS
                writer.close()
                ctx.psx_streams = None
            if ctx.psx_status == CONNECTION_TENTATIVE_STATUS:
                if not error_status:
                    logger.info("Successfully Connected to psx")
                    ctx.psx_status = CONNECTION_CONNECTED_STATUS
                else:
                    ctx.psx_status = f"Was tentatively connected but error occured: {error_status}"
            elif error_status:
                ctx.psx_status = error_status
                logger.info("Lost connection to psx and attempting to reconnect. Use /psx for status updates")
        else:
            try:
                logger.debug("Attempting to connect to psx")
                ctx.psx_streams = await asyncio.wait_for(asyncio.open_connection("localhost", 52980), timeout=10)
                ctx.psx_status = CONNECTION_TENTATIVE_STATUS
            except TimeoutError:
                logger.debug("Connection Timed Out, Trying Again")
                ctx.psx_status = CONNECTION_TIMING_OUT_STATUS
                continue
            except ConnectionRefusedError:
                logger.debug("Connection Refused, Trying Again")
                ctx.psx_status = CONNECTION_REFUSED_STATUS
                continue


async def parse_locations(locations_array: typing.List[int], ctx: SOTNContext, force: bool):
    if locations_array == ctx.locations_array and not force:
        return
    else:
        ctx.locations_array = locations_array
        locations_checked = []

        for location in ctx.missing_locations:
            index = location
            if location in locations_array:
                locations_checked.append(location)

        if locations_checked:
            await ctx.send_msgs([
                {"cmd": "LocationChecks",
                 "locations": locations_checked}
            ])
    return

async def check_victory(payload : str, ctx: SOTNContext):
    if payload == 'True' and not ctx.finished_game:
        await ctx.send_msgs([{
            "cmd": "StatusUpdate",
            "status": 30
        }])
        ctx.finished_game = True


if __name__ == '__main__':
    gui_enabled = not sys.stdout or "--nogui" not in sys.argv

    Utils.init_logging("SOTNClient")

    async def main(args):
        multiprocessing.freeze_support()

        ctx = SOTNContext(args.connect, args.password)
        ctx.server_task = asyncio.create_task(server_loop(ctx), name="ServerLoop")

        if gui_enabled:
            ctx.run_gui()
        ctx.run_cli()
        ctx.psx_sync_task = asyncio.create_task(psx_sync_task(ctx), name="PSX Sync")

        await ctx.exit_event.wait()

        ctx.server_address = None

        await ctx.shutdown()

        if ctx.psx_sync_task:
            await ctx.psx_sync_task

    import colorama

    parser = get_base_parser()
    args = parser.parse_args()

    colorama.init()

    asyncio.run(main(args))
    colorama.deinit()
