"""即点歌"""
from nonebot import on_command
from nonebot.params import CommandArg, Arg
from nonebot.matcher import Matcher
from nonebot.adapters.onebot.v11 import Message

from .data_source import search_cloud, search_tencent


siren = on_command("塞壬点歌", block=True)


@siren.handle()
async def _(matcher: Matcher, args: Message = CommandArg()):
    args = args.extract_plain_text().strip()
    if args:
        matcher.set_arg("keywords", args)


@siren.got(key="keywords", prompt="请发送要点的歌名:")
async def _(keywords: str = Arg()):
    await siren.send("搜索中...")
    await siren.finish(
        await search_cloud(keywords)
    )


__zx_plugin_name__ = "塞壬点歌"
__plugin_usage__ = """
usage:
    即网易云点歌
    指令：
        塞壬点歌 [歌曲名] => 点歌，以卡片形式发到群内
""".strip()
__plugin_des__ = "即网易云点歌"
__plugin_cmd__ = ["塞壬点歌"]
__plugin_settings__ = {
    "cmd": ["塞壬点歌"]
}
__plugin_type__ = ("方舟相关", 1)
__plugin_version__ = 1.0
__plugin_author__ = "Number_Sir<number_sir@126.com>"
