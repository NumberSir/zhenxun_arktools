# from .game_guess_operator import *  # 猜干员
#
# from .misc_monster_siren import *  # 点歌
# from .misc_operator_birthday import *  # 生日提醒
#
# from .tool_open_recruitment import *  # 公招识别
# from .tool_operator_info import *  # 干员信息
# from .tool_sanity_notify import *  # 理智回复

from .utils import *
import nonebot
from pathlib import Path

nonebot.load_plugin(Path(__file__).parent / "game_guess_operator")
nonebot.load_plugin(Path(__file__).parent / "misc_monster_siren")
nonebot.load_plugin(Path(__file__).parent / "misc_operator_birthday")
nonebot.load_plugin(Path(__file__).parent / "tool_open_recruitment")
nonebot.load_plugin(Path(__file__).parent / "tool_operator_info")
nonebot.load_plugin(Path(__file__).parent / "tool_sanity_notify")
nonebot.load_plugin(Path(__file__).parent / "tool_announce_push")
nonebot.load_plugin(Path(__file__).parent / "tool_fetch_maa_copilot")
