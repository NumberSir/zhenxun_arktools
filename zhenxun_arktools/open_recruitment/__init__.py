"""公招一四五六星推荐"""
from nonebot import on_command
from nonebot.adapters.onebot.v11 import Message
from nonebot.params import CommandArg

from services.log import logger
from .data_source import get_recommend_tags

__zx_plugin_name__ = "方舟公招推荐"
__plugin_usage__ = """
usage：
    输入公招tag来看看哪些组合会出一四五六星干员
    指令：
        公开招募 [标签1 标签2 ...]
""".strip()
__plugin_des__ = "输入公招tag来看看哪些组合会出一四五六星干员"
__plugin_cmd__ = ["公开招募"]
__plugin_type__ = ("方舟相关",)
__plugin_version__ = 0.2
__plugin_author__ = "Number_Sir"
__plugin_settings__ = {
    "level": 5,
    "default_status": True,
    "limit_superuser": False,
    "cmd": ["公开招募"],
}

recruit = on_command("公开招募", aliases={"公招", "方舟公招", "公招tag"}, priority=5, block=True)


@recruit.handle()
async def _(arg: Message = CommandArg()):
    logger.info(f"{arg}")
    taglist = arg.extract_plain_text().strip().split()
    rst = await get_recommend_tags(taglist)

    if rst is None:
        rst = f"获取公招推荐数据失败！请检查网络连接并稍后重试"

    if not rst:
        rst = f"当前没有必出稀有干员的公招标签"

    await recruit.finish(rst, at_sender=True)