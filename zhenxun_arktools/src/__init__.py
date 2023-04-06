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


"""OCR_CONFIG"""
Config.add_plugin_config(
    module="zhenxun_arktools",
    key="ARKNIGHTS_BAIDU_API_KEY",
    name="zhenxun_arktools",
    value="",
    help_="百度 OCR API KEY, 详见https://console.bce.baidu.com/ai/?fromai=1#/ai/ocr/app/list",
    default_value=""
)
Config.add_plugin_config(
    module="zhenxun_arktools",
    key="ARKNIGHTS_BAIDU_SECRET_KEY",
    name="zhenxun_arktools",
    value="",
    help_="百度 OCR SECRET KEY, 详见https://console.bce.baidu.com/ai/?fromai=1#/ai/ocr/app/list",
    default_value=""
)

"""PATH_CONFIG"""
Config.add_plugin_config(
    module="zhenxun_arktools",
    key="ARKNIGHTS_DATA_PATH",
    name="zhenxun_arktools",
    value="data/arktools",
    help_="舟舟插件资源根目录，修改这个则其它路径都要修改",
    default_value="data/arktools"
)
Config.add_plugin_config(
    module="zhenxun_arktools",
    key="ARKNIGHTS_FONT_PATH",
    name="zhenxun_arktools",
    value="data/arktools/fonts",
    help_="舟舟插件字体目录",
    default_value="data/arktools/fonts"
)
Config.add_plugin_config(
    module="zhenxun_arktools",
    key="ARKNIGHTS_GAMEDATA_PATH",
    name="zhenxun_arktools",
    value="data/arktools/arknights/gamedata",
    help_="舟舟插件游戏数据目录",
    default_value="data/arktools/arknights/gamedata"
)
Config.add_plugin_config(
    module="zhenxun_arktools",
    key="ARKNIGHTS_GAMEIMAGE_PATH",
    name="zhenxun_arktools",
    value="data/arktools/arknights/gameimage",
    help_="舟舟插件游戏图片目录",
    default_value="data/arktools/arknights/gameimage"
)
Config.add_plugin_config(
    module="zhenxun_arktools",
    key="ARKNIGHTS_DB_URL",
    name="zhenxun_arktools",
    value="data/arktools/databases/arknights_sqlite.sqlite3",
    help_="舟舟插件数据库目录",
    default_value="data/arktools/databases/arknights_sqlite.sqlite3"
)

"""PROXY_CONFIG"""
Config.add_plugin_config(
    module="zhenxun_arktools",
    key="GITHUB_RAW",
    name="zhenxun_arktools",
    value="https://raw.githubusercontent.com",
    help_="https://raw.githubusercontent.com 的镜像站",
    default_value="https://raw.githubusercontent.com"
)
Config.add_plugin_config(
    module="zhenxun_arktools",
    key="GITHUB_SITE",
    name="zhenxun_arktools",
    value="https://github.com",
    help_="https://github.com 的镜像站",
    default_value="https://github.com"
)
Config.add_plugin_config(
    module="zhenxun_arktools",
    key="RSS_SITE",
    name="zhenxun_arktools",
    value="https://rsshub.app",
    help_="https://rsshub.app 的镜像站",
    default_value="https://rsshub.app"
)

"""SCHEDULER_CONFIG"""
Config.add_plugin_config(
    module="zhenxun_arktools",
    key="ANNOUNCE_PUSH_SWITCH",
    name="zhenxun_arktools",
    value=False,
    help_="自动获取 & 推送舟舟最新公告开关",
    default_value=False
)
Config.add_plugin_config(
    module="zhenxun_arktools",
    key="ANNOUNCE_PUSH_INTERVAL",
    name="zhenxun_arktools",
    value=1,
    help_="自动获取 & 推送舟舟最新公告间隔多少分钟运行一次",
    default_value=1
)
Config.add_plugin_config(
    module="zhenxun_arktools",
    key="SANITY_NOTIFY_SWITCH",
    name="zhenxun_arktools",
    value=False,
    help_="检测理智提醒开关",
    default_value=False
)
Config.add_plugin_config(
    module="zhenxun_arktools",
    key="SANITY_NOTIFY_INTERVAL",
    name="zhenxun_arktools",
    value=10,
    help_="检测理智提醒间隔多少分钟运行一次",
    default_value=10
)
Config.add_plugin_config(
    module="zhenxun_arktools",
    key="ARKNIGHTS_UPDATE_CHECK_SWITCH",
    name="zhenxun_arktools",
    value=True,
    help_="启动bot时检测素材更新开关",
    default_value=True
)
