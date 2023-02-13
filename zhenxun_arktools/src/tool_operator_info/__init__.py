"""
获取干员信息：
1. 技能 1~7 升级材料 √
2. 精英化材料 √
3. 技能专精材料 √
4. 模组升级材料 √
5. 模组任务
6. 基本信息: HandbookInfo
"""
from nonebot import on_command
from nonebot.plugin import PluginMetadata
from nonebot.params import CommandArg
from nonebot.adapters.onebot.v11 import Message, MessageSegment

from .data_source import BuildOperatorInfo
from ..core.models_v3 import Character
from ..exceptions import *

operator_info = on_command("方舟干员", aliases={"干员"})


@operator_info.handle()
async def _(arg: Message = CommandArg()):
    name = arg.extract_plain_text().strip()
    if not name:
        await operator_info.finish()

    try:
        cht = await Character.parse_name(name)
    except NamedCharacterNotExistException as e:
        await operator_info.finish(e.msg, at_sender=True)

    img_bytes = await BuildOperatorInfo(cht=cht).build_whole_image()
    await operator_info.finish(MessageSegment.image(img_bytes))


__zx_plugin_name__ = "干员信息"
__plugin_usage__ = """
usage:
    查看干员精英化、技能升级、技能专精、模组解锁需要的材料
    指令:
        干员 [干员名称] => 查看对应干员的材料
""".strip()
__plugin_des__ = "查看干员精英化、技能升级、技能专精、模组解锁需要的材料"
__plugin_cmd__ = ["干员/方舟干员"]
__plugin_settings__ = {
    "cmd": ["干员/方舟干员"]
}
__plugin_type__ = ("方舟相关", 1)
__plugin_version__ = 1.0
__plugin_author__ = "Number_Sir<number_sir@126.com>"
