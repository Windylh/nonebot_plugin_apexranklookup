from nonebot import get_driver
from nonebot.plugin import MatcherGroup
from nonebot.adapters import Event
from nonebot.typing import T_State
from nonebot.adapters.onebot.v11 import Message
from nonebot.adapters.onebot.v11 import MessageEvent
from nonebot.exception import ActionFailed


from loguru import logger

from .api import apexApi
from .config import Config

global_config = get_driver().config
config = Config.parse_obj(global_config)

worker = MatcherGroup(type="message", block=True, priority=10)
rank = worker.on_command((".stat", ".查询"))
maps = worker.on_command(".map", aliases={".地图"})
predator = worker.on_command(".猎杀", aliases={".pd"})
store = worker.on_command(".复制器", aliases={".crafting"})


apexApi = apexApi(config.apex_api_token)


@rank.handle()
async def query_rank(event: Event, state: T_State):
    if isinstance(event, MessageEvent):
        try:
            raw = event.get_plaintext().lstrip(".stat").lstrip(".查询").strip().split(" ")
            if not raw or raw == ['']:
                await maps.send("请输入.查询/.stat origin_id 以空格隔开。")
                return
            if len(raw) > 1:
                origin_id, platform = raw
            else:
                origin_id = raw[0]
                platform = "PC"
            await maps.send("正在查询，请稍等。")
            msg = apexApi.player_query(origin_id, platform)
            await maps.finish(Message(msg))
        except ActionFailed as e:
            logger.warning(
                f"ActionFailed {e.info['retcode']} {e.info['msg'].lower()} {e.info['wording']}"
            )
    else:
        logger.warning("Not supported: nbnhhsh")


@maps.handle()
async def query_map(event: Event, state: T_State):
    if isinstance(event, MessageEvent):
        try:
            await maps.send("正在查询，请稍等。")
            msg = apexApi.map_query()
            await maps.finish(Message(msg))
        except ActionFailed as e:
            logger.warning(
                f"ActionFailed {e.info['retcode']} {e.info['msg'].lower()} {e.info['wording']}"
            )
    else:
        logger.warning("Not supported: apexranklookup")


@predator.handle()
async def query_predator(event: Event, state: T_State):
    if isinstance(event, MessageEvent):
        try:
            await maps.send("正在查询，请稍等。")
            msg = apexApi.predator()
            await maps.finish(Message(msg))
        except ActionFailed as e:
            logger.warning(
                f"ActionFailed {e.info['retcode']} {e.info['msg'].lower()} {e.info['wording']}"
            )
    else:
        logger.warning("Not supported: apexranklookup")


@store.handle()
async def query_store(event: Event, state: T_State):
    if isinstance(event, MessageEvent):
        try:
            await maps.send("正在查询，请稍等。")
            msg = apexApi.store_query()
            await maps.finish(Message(msg))
        except ActionFailed as e:
            logger.warning(
                f"ActionFailed {e.info['retcode']} {e.info['msg'].lower()} {e.info['wording']}"
            )
    else:
        logger.warning("Not supported: apexranklookup")
