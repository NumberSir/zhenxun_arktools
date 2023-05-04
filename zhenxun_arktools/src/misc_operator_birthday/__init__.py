"""干员生日提醒"""
from pathlib import Path

from nonebot import on_command, logger
from nonebot.adapters.onebot.v11 import MessageSegment, Message
from typing import List
from datetime import datetime
from PIL import Image, ImageFont
from PIL.ImageDraw import Draw
from io import BytesIO

from ..core.models_v3 import Character
from ..exceptions import NoHandbookInfoException
from ..utils import text_border
from configs.config import Config

font_path = Path(Config.get_config("zhenxun_arktools", "ARKNIGHTS_FONT_PATH")).absolute()


today_birthday = on_command("今日干员", block=True)


@today_birthday.handle()
async def _():
    today = datetime.now().strftime("%m月%d日").strip("0").replace("月0", "月")
    characters = await Character.all()
    try:
        results: List["Character"] = [
            cht
            for cht in characters
            if (await cht.get_handbook_info()).story_text_audio.birthday == today
        ]
    except NoHandbookInfoException as e:
        await today_birthday.finish(f"嗯唔……干员的档案数据不全哦")

    if not results:
        await today_birthday.finish("哦呀？今天没有干员过生日哦……")
    try:
        main_background = Image.new("RGBA", (24*2+128*len(results)+16*(len(results)-1), 24*2+128+24), (0, 0, 0, 0))
        for idx, cht in enumerate(results):
            cht_bg = Image.new("RGBA", (128, 128+24), (150, 150, 150, 150))
            icon = cht.avatar.convert("RGBA").resize((128, 128))
            cht_bg.paste(im=icon, box=(0, 0), mask=icon.split()[3])
            text_border(
                cht.name,
                Draw(cht_bg),
                x=64,
                y=(128 + 12 + 152 * (idx // 6)),
                anchor="mm",
                font=ImageFont.truetype((font_path / "Arknights-zh.otf").__str__(), 20),
                fill_colour=(255, 255, 255, 255),
                shadow_colour=(0, 0, 0, 255)
            )
            main_background.paste(cht_bg, (24+idx*(128+16), 24), mask=cht_bg.split()[3])
    except FileNotFoundError as e:
        logger.error("干员信息缺失，请使用 “更新方舟素材” 命令更新游戏素材后重试")
        await today_birthday.finish("干员信息缺失，请使用 “更新方舟素材” 命令更新游戏素材后重试")

    output = BytesIO()
    main_background.save(output, format="png")
    await today_birthday.finish(
        Message(
            MessageSegment.image(output) +
            "\n今天过生日的干员有这些哦"
        )
    )


__zx_plugin_name__ = "今日干员"
__plugin_usage__ = """
usage:
    查看今日过生日的干员
    指令:
        今日干员 => 查看今日过生日的干员
""".strip()
__plugin_des__ = "查看今日过生日的干员"
__plugin_cmd__ = ["今日干员"]
__plugin_settings__ = {
    "cmd": ["今日干员"]
}
__plugin_type__ = ("方舟相关", 1)
__plugin_version__ = 1.0
__plugin_author__ = "Number_Sir<number_sir@126.com>"
