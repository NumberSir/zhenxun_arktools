"""公招筛选"""
import httpx
from nonebot import on_command, logger
from nonebot.params import Arg, RawCommand
from nonebot.typing import T_State
from nonebot.matcher import Matcher
from nonebot.exception import ActionFailed
from nonebot.adapters.onebot.v11 import Message, MessageSegment, MessageEvent

from typing import Union

from .data_source import BuildRecruitmentCard, process_word_tags, baidu_ocr


recruit = on_command("公招", aliases={"公开招募"}, block=True)


@recruit.handle()
async def _(state: T_State, event: MessageEvent, matcher: Matcher, raw: str = RawCommand()):
    if event.reply:
        event.message = event.reply.message

    if event.message.get("image", None):  # 自带图片
        logger.debug("发送公招截图")
        for img in event.message["image"]:
            img_url = img.data.get("url", "")
            state["recruit"] = "image"
            matcher.set_arg("rec", img_url)

    elif event.message.extract_plain_text().replace(raw, "").strip():  # 文字tag
        tags = event.message.extract_plain_text().replace(raw, "").strip()
        logger.debug("直接输入文字标签")
        state["recruit"] = "str"
        matcher.set_arg("rec", tags)


@recruit.got(key="rec", prompt="请发送公招截图:")
async def _(state: T_State, rec: Union[Message, str] = Arg()):
    if state.get("recruit", None) == "str":  # 文字输入
        tags = set(process_word_tags(rec.split()))
    else:
        if isinstance(rec, Message):
            img_url = rec["image"][0].data.get("url", "")
        else:
            img_url = rec
        await recruit.send("识别中...")
        async with httpx.AsyncClient() as client:
            try:
                tags = await baidu_ocr(image_url=img_url, client=client)
            except FileNotFoundError as e:
                logger.error("干员信息缺失，请使用 “更新方舟素材” 命令更新游戏素材后重试")
                await recruit.finish("公招标签文件缺失，请使用 “更新方舟素材” 命令更新游戏素材后重试")

    if tags is None:
        await recruit.finish("百度OCR出错，请检查运行日志！", at_sender=True)
    if not tags:
        await recruit.finish("没有检测到符合要求的公招标签！", at_sender=True)
    logger.debug(f"tags: {tags}")
    await recruit.send(f"检测到的公招标签：{', '.join(list(tags))}")

    try:
        recruit_list = await BuildRecruitmentCard.build_target_characters(tags)
    except FileNotFoundError as e:
        logger.error("干员信息缺失，请使用 “更新方舟素材” 命令更新游戏素材后重试")
        await recruit.finish("干员信息缺失，请使用 “更新方舟素材” 命令更新游戏素材后重试")

    if not recruit_list:
        await recruit.finish("没有必出稀有干员的标签组合哦！", at_sender=True)
    draw = BuildRecruitmentCard(recruit_list)
    image = draw.build_main()
    img = MessageSegment.image(image)
    try:
        await recruit.finish(Message(img))
    except ActionFailed as e:
        await recruit.finish(f"图片发送失败：{e}")


__zx_plugin_name__ = "公开招募"
__plugin_usage__ = """
usage:
    查看公招标签可能出的稀有干员组合
    指令：
        公招 [公招界面截图] => 查看标签组合及可能出现的干员
        回复公招界面截图：公招 => 同上
        公招 [标签1] [标签2] ... => 同上
""".strip()
__plugin_des__ = "查看公招标签可能出的稀有干员组合"
__plugin_cmd__ = ["公招", "公开招募", "方舟公招"]
__plugin_settings__ = {
    "cmd": ["公招", "公开招募", "方舟公招"]
}
__plugin_type__ = ("方舟相关", 1)
__plugin_version__ = 1.0
__plugin_author__ = "Number_Sir<number_sir@126.com>"
