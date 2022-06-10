import requests
import json
from nonebot.adapters.onebot.v11 import MessageSegment


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
            r = requests.get(f"{self.url}/bridge?auth={self.api_key}&player={user_id}&platform={platform}&merge=True&removeMerged=True")
        except Exception:
            return "网络爆炸了，请稍后重试或联系管理员"
        result = json.loads(r.text)
        if result.get("Error"):
            return result.get("Error")
        msg = f"""Id：{result.get("global").get("name")}
等级：{result.get("global").get("level")}
当前段位：{str(MessageSegment.image(result.get("global").get("rank").get("rankImg")))}
当前分数：{result.get("global").get("rank").get("rankScore")}
当前竞技场段位：{str(MessageSegment.image(result.get("global").get("arena").get("rankImg")))}
当前竞技场分数：{result.get("global").get("arena").get("rankScore")}
当前状态：{result.get("realtime").get("currentStateAsText")}"""
        return msg

    def map_query(self):
        try:
            r = requests.get(f"{self.url}/maprotation?auth={self.api_key}&version=2")
        except Exception:
            return "网络爆炸了，请稍后重试或联系管理员"
        result = json.loads(r.text)
        if result.get("Error"):
            return result.get("Error")
        msg = f"""大逃杀：
当前地图：{result.get("battle_royale").get("current").get("map")}
剩余时间：{result.get("battle_royale").get("current").get("remainingTimer")}
下一张地图：{result.get("battle_royale").get("next").get("map")}
积分联赛：
当前地图：{result.get("ranked").get("current").get("map")}
下赛季地图：{result.get("ranked").get("next").get("map")}
竞技场：
当前地图：{str(MessageSegment.image(result.get("arenas").get("current").get("asset")))}
剩余时间：{result.get("arenas").get("current").get("remainingTimer")}
下一张地图：{str(MessageSegment.image(result.get("arenas").get("next").get("asset")))}"""
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
竞技场：
PC: 最低分 {result.get("AP").get("PC").get("val")}, 大师 {result.get("AP").get("PC").get("totalMastersAndPreds")}
PS: 最低分 {result.get("AP").get("PS4").get("val")}, 大师 {result.get("AP").get("PS4").get("totalMastersAndPreds")}
Xbox: 最低分 {result.get("AP").get("X1").get("val")}, 大师 {result.get("AP").get("X1").get("totalMastersAndPreds")}
Switch: 最低分 {result.get("AP").get("SWITCH").get("val")}, 大师 {result.get("AP").get("SWITCH").get("totalMastersAndPreds")}"""
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
    pass
