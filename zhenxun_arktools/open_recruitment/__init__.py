"""公招一四五六星推荐"""
from nonebot import on_command
from nonebot.adapters.onebot.v11 import Message, GroupMessageEvent, MessageSegment
from nonebot.exception import ActionFailed
from nonebot.internal.params import Arg
from nonebot.matcher import Matcher

from services.log import logger
from .data_source import ocr, get_rare_operators, build_image

__zx_plugin_name__ = "方舟公招推荐"
__plugin_usage__ = """
usage：
    发送公招界面截图来看看哪些组合会出一四五六星干员
    指令：
        公招[截图]
        回复公招截图消息：公招
        公招，发送公招截图
""".strip()
__plugin_des__ = "输入公招tag来看看哪些组合会出一四五六星干员"
__plugin_cmd__ = ["公招", "方舟公招", "公开招募"]
__plugin_type__ = ("方舟相关",)
__plugin_version__ = 0.3
__plugin_author__ = "Number_Sir"
__plugin_settings__ = {
    "level": 5,
    "default_status": True,
    "limit_superuser": False,
    "cmd": ["公招", "方舟公招", "公开招募"],
}
__plugin_configs__ = {
    "TENCENT_CLOUD_SECRET_ID": {
        "value": "",
        "help": "使用 OCR 功能需要填写的腾讯开发者 SecretId, 见 https://console.cloud.tencent.com/",
        "default_value": ""
    },
    "TENCENT_CLOUD_SECRET_KEY": {
        "value": "",
        "help": "使用 OCR 功能需要填写的腾讯开发者 SecretKey, 见 https://console.cloud.tencent.com/",
        "default_value": ""
    }
}

recruit = on_command("公招", aliases={"方舟公招", "公开招募"}, priority=5, block=True)


@recruit.handle()
async def _(matcher: Matcher, event: GroupMessageEvent):
    if event.reply:
        event.message = event.reply.message

    if event.message.get("image", None):  # 自带图片
        for img in event.message["image"]:
            img_url = img.data.get("url", "")
            matcher.set_arg("image", img_url)


@recruit.got(key="image", prompt="请发送公招截图:")
async def _(image: Message = Arg()):
    logger.info(f"image: {image}")
    if isinstance(image, str):
        img_url = image
    else:
        img_url = image["image"][0].data.get("url", "")
    await recruit.send("识别中...")
    tags = ocr(image_url=img_url)
    recruit_list = get_rare_operators(tags)
    if not recruit_list:
        await recruit.finish("没有必出稀有干员的标签组合哦！", at_sender=True)
    image = build_image(recruit_list)
    img = MessageSegment.image(image)
    try:
        await recruit.finish(Message(img))
    except ActionFailed as e:
        await recruit.finish(f"图片发送失败：{e}")