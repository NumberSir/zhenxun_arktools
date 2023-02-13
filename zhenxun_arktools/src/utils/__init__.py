"""一些功能吧"""
from .general import *
from .image import *
from .database import *
from .update import *

from nonebot import on_command
from nonebot.plugin import PluginMetadata
import httpx


update_game_resource = on_command("更新方舟素材")
init_db = on_command("更新方舟数据库")


@update_game_resource.handle()
async def _():
    await update_game_resource.send("开始更新游戏素材……")
    async with httpx.AsyncClient() as client:
        await ArknightsGameData(client).download_files()
        await ArknightsDB.init_data()
        await ArknightsGameImage(client).download_files()
    await update_game_resource.finish("游戏数据更新完成！")


@init_db.handle()
async def _():
    await update_game_resource.send("开始更新游戏数据库……")
    await ArknightsDB.init_data()
    await update_game_resource.finish("游戏数据库更新完成！")


__zx_plugin_name__ = "方舟杂项"
__plugin_usage__ = """
usage:
    手动更新游戏素材、更新本地数据库
    指令:
        更新方舟素材 => 从Github下载游戏素材(json数据与图片)
        更新方舟数据库 => 更新本地sqlite数据库
""".strip()
__plugin_des__ = "更新游戏素材、更新本地数据库"
__plugin_cmd__ = ["更新方舟素材", "更新方舟数据库"]
__plugin_settings__ = {
    "cmd": ["更新方舟素材", "更新方舟数据库"]
}
__plugin_type__ = ("方舟相关", 1)
__plugin_version__ = 1.0
__plugin_author__ = "Number_Sir<number_sir@126.com>"
