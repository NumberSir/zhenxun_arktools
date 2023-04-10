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

nonebot.load_plugin((Path(__file__).parent / "game_guess_operator").__str__())
nonebot.load_plugin((Path(__file__).parent / "misc_monster_siren").__str__())
nonebot.load_plugin((Path(__file__).parent / "misc_operator_birthday").__str__())
nonebot.load_plugin((Path(__file__).parent / "tool_open_recruitment").__str__())
nonebot.load_plugin((Path(__file__).parent / "tool_operator_info").__str__())
nonebot.load_plugin((Path(__file__).parent / "tool_sanity_notify").__str__())
nonebot.load_plugin((Path(__file__).parent / "tool_announce_push").__str__())
