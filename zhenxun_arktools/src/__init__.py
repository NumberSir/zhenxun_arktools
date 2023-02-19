# from .game_guess_operator import *  # 猜干员
#
# from .misc_monster_siren import *  # 点歌
# from .misc_operator_birthday import *  # 生日提醒
#
# from .tool_open_recruitment import *  # 公招识别
# from .tool_operator_info import *  # 干员信息
# from .tool_sanity_notify import *  # 理智回复

from .utils import *
from configs.config import Config
import nonebot
from pathlib import Path

nonebot.load_plugin(Path(__file__).parent / "game_guess_operator")
nonebot.load_plugin(Path(__file__).parent / "misc_monster_siren")
nonebot.load_plugin(Path(__file__).parent / "misc_operator_birthday")
nonebot.load_plugin(Path(__file__).parent / "tool_open_recruitment")
nonebot.load_plugin(Path(__file__).parent / "tool_operator_info")
nonebot.load_plugin(Path(__file__).parent / "tool_sanity_notify")
nonebot.load_plugin(Path(__file__).parent / "tool_announce_push")


Config.add_plugin_config(
    module="zhenxun_arktools",
    key="arknights_baidu_app_id",
    name="zhenxun_arktools",
    value="",
    help_="百度 OCR APP ID, 详见https://console.bce.baidu.com/ai/?fromai=1#/ai/ocr/app/list",
    default_value=""
)
Config.add_plugin_config(
    module="zhenxun_arktools",
    key="arknights_baidu_api_key",
    name="zhenxun_arktools",
    value="",
    help_="百度 OCR API KEY, 详见https://console.bce.baidu.com/ai/?fromai=1#/ai/ocr/app/list",
    default_value=""
)
Config.add_plugin_config(
    module="zhenxun_arktools",
    key="github_raw",
    name="zhenxun_arktools",
    value="https://raw.githubusercontent.com",
    help_="https://raw.githubusercontent.com 的镜像站",
    default_value="https://raw.githubusercontent.com"
)
Config.add_plugin_config(
    module="zhenxun_arktools",
    key="github_site",
    name="zhenxun_arktools",
    value="https://github.com",
    help_="https://github.com 的镜像站",
    default_value="https://github.com"
)
Config.add_plugin_config(
    module="zhenxun_arktools",
    key="announce_push_switch",
    name="zhenxun_arktools",
    value=False,
    help_="https://github.com 的镜像站",
    default_value=False
)
Config.add_plugin_config(
    module="zhenxun_arktools",
    key="announce_push_interval",
    name="zhenxun_arktools",
    value=1,
    help_="https://github.com 的镜像站",
    default_value=1
)
Config.add_plugin_config(
    module="zhenxun_arktools",
    key="sanity_notify_switch",
    name="zhenxun_arktools",
    value=False,
    help_="https://github.com 的镜像站",
    default_value=False
)
Config.add_plugin_config(
    module="zhenxun_arktools",
    key="sanity_notify_interval",
    name="zhenxun_arktools",
    value=10,
    help_="https://github.com 的镜像站",
    default_value=10
)
