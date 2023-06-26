from nonebot import get_driver
from nonebot.plugin import MatcherGroup
from nonebot.adapters import Event
from nonebot.typing import T_State
from nonebot.adapters.onebot.v11 import Message
from nonebot.adapters.onebot.v11 import MessageEvent
from nonebot.exception import ActionFailed

from loguru import logger
import os, json

from .api import apexApi
from .config import Config

bot = get_driver()
global_config = get_driver().config
config = Config.parse_obj(global_config)

worker = MatcherGroup(type="message", block=True, priority=10)
rank = worker.on_command(".stat", aliases={".查询"})
maps = worker.on_command(".map", aliases={".地图"})
predator = worker.on_command(".猎杀", aliases={".pd"})
store = worker.on_command(".复制器", aliases={".crafting"})
bind = worker.on_command(".绑定", aliases={".bind"})
unbind = worker.on_command(".解绑", aliases={".unbind"})

apexApi = apexApi(config.apex_api_token)
dirname, filename = os.path.split(os.path.abspath(__file__))

user_info = {}


@bot.on_startup
async def load_userinfo():
    global user_info
    with open(f"{dirname}/data/user_info.json", "r") as f:
        user_info = json.load(f)


@rank.handle()
async def query_rank(event: Event, state: T_State):
    if isinstance(event, MessageEvent):
        try:
            raw = event.get_plaintext().lstrip(".stat").lstrip(".查询").strip().split(" ")
            if (not raw or raw == ['']) and not user_info.get(event.get_user_id()):
                await rank.send("请输入.查询/.stat origin_id 平台代码(xbox、ps、pc默认pc) 以空格隔开。")
                return
            elif user_info.get(event.get_user_id()):
                raw = user_info.get(event.get_user_id())
            if len(raw) > 1:
                origin_id, platform = raw
            else:
                origin_id = raw[0]
                platform = "PC"
            await rank.send("正在查询，请稍等。")
            msg = apexApi.player_query(origin_id, platform)
            await rank.finish(Message(msg))
        except ActionFailed as e:
            logger.warning(
                f"ActionFailed {e.info['retcode']} {e.info['msg'].lower()} {e.info['wording']}"
            )
    else:
        logger.warning("Not supported: apexranklookup")


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
            await predator.send("正在查询，请稍等。")
            msg = apexApi.predator()
            await predator.finish(Message(msg))
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
            await store.send("正在查询，请稍等。")
            msg = apexApi.store_query()
            await store.finish(Message(msg))
        except ActionFailed as e:
            logger.warning(
                f"ActionFailed {e.info['retcode']} {e.info['msg'].lower()} {e.info['wording']}"
            )
    else:
        logger.warning("Not supported: apexranklookup")


@bind.handle()
async def bind_user(event: Event, state: T_State):
    if isinstance(event, MessageEvent):
        try:
            raw = event.get_plaintext().lstrip(".bind").lstrip(".绑定").strip().split(" ")
            if user_info.get(event.get_user_id()):
                await bind.send(f"您已经绑定过了")
                return
            elif not raw or raw == ['']:
                await bind.send("请输入.bind/.绑定 origin_id 平台代码(xbox、ps、pc默认pc) 以空格隔开。")
                return
            if len(raw) > 1:
                origin_id, platform = raw
            else:
                origin_id = raw[0]
                platform = "PC"
            await bind.send("正在绑定，请稍等。")
            msg = apexApi.player_query(origin_id, platform)
            if msg.startswith("Error"):
                await bind.finish(Message("绑定失败。\n"+msg))
            else:
                user_info[event.get_user_id()] = raw
                with open(f"{dirname}/data/user_info.json", "w") as f:
                    json.dump(user_info, f)
                await bind.finish(Message("绑定成功。\n" + msg))
        except ActionFailed as e:
            logger.warning(
                f"ActionFailed {e.info['retcode']} {e.info['msg'].lower()} {e.info['wording']}"
            )
    else:
        logger.warning("Not supported: apexranklookup")


@unbind.handle()
async def unbind_user(event: Event, state: T_State):
    if isinstance(event, MessageEvent):
        try:
            if not user_info.get(event.get_user_id()):
                await unbind.send(f"您还没绑定过。")
                return
            del user_info[event.get_user_id()]
            with open(f"{dirname}/data/user_info.json", "w") as f:
                json.dump(user_info, f)
            await unbind.finish(Message("解绑成功。"))
        except ActionFailed as e:
            logger.warning(
                f"ActionFailed {e.info['retcode']} {e.info['msg'].lower()} {e.info['wording']}"
            )
    else:
        logger.warning("Not supported: apexranklookup")