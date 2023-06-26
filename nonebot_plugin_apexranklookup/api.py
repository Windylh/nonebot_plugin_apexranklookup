import requests
import json
from nonebot.adapters.onebot.v11 import MessageSegment
from .draw import *


class apexApi:
    def __init__(self, api_key):
        self.url = "https://api.mozambiquehe.re"
        self.api_key = api_key

    def player_query(self, user_id, platform):
        if platform.lower() == "xbox":
            platform = "X1"
        elif "ps" in platform.lower():
            platform = "PS4"
        elif platform.lower() == "pc":
            platform = "PC"
        else:
            return "请输入正确的平台(pc,xbox,ps)"
        try:
            r = requests.get(f"{self.url}/bridge?auth={self.api_key}&player={user_id}&platform={platform}&merge=True&removeMerged=True&version=5")
        except Exception:
            return "Error:" + "网络爆炸了，请稍后重试或联系管理员"
        result = json.loads(r.text)
        if result.get("Error"):
            return "Error: " + result.get("Error")
        msg = str(MessageSegment.image(draw_profile(result)))
        return msg

    def map_query(self):
        try:
            r = requests.get(f"{self.url}/maprotation?auth={self.api_key}&version=2")
        except Exception:
            return "网络爆炸了，请稍后重试或联系管理员"
        result = json.loads(r.text)
        if result.get("Error"):
            return result.get("Error")
        msg = MessageSegment.image(draw_map(result))
        return msg

    def predator(self):
        try:
            r = requests.get(f"{self.url}/predator?auth={self.api_key}")
        except Exception:
            return "网络爆炸了，请稍后重试或联系管理员"
        result = json.loads(r.text)
        if result.get("Error"):
            return result.get("Error")
        msg = f"""大逃杀：
PC: 最低分 {result.get("RP").get("PC").get("val")}, 大师 {result.get("RP").get("PC").get("totalMastersAndPreds")}
PS: 最低分 {result.get("RP").get("PS4").get("val")}, 大师 {result.get("RP").get("PS4").get("totalMastersAndPreds")}
Xbox: 最低分 {result.get("RP").get("X1").get("val")}, 大师 {result.get("RP").get("X1").get("totalMastersAndPreds")}
Switch: 最低分 {result.get("RP").get("SWITCH").get("val")}, 大师 {result.get("RP").get("SWITCH").get("totalMastersAndPreds")}
"""
        return msg

    def store_query(self):
        try:
            r = requests.get(f"{self.url}/crafting?auth={self.api_key}")
        except Exception:
            return "网络爆炸了，请稍后重试或联系管理员"
        result = json.loads(r.text)
        msg = f"""当前复制器:
{" ".join(str(MessageSegment.image(i.get("itemType").get("asset"))) for i in result[0].get("bundleContent"))}
{" ".join(str(MessageSegment.image(i.get("itemType").get("asset"))) for i in result[1].get("bundleContent"))}"""
        return msg


if __name__ == "__main__":
    api = apexApi("")
    # api.player_query("Paradisesssssa", "PC")
    # api.player_query("TTV_WeThePeople1", "PC")
    api.map_query()
