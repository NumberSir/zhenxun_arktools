"""理智恢复提醒"""
from datetime import datetime

import tortoise.exceptions
from nonebot import on_command, get_bot, logger, get_driver
from nonebot.adapters.onebot.v11 import GroupMessageEvent, MessageEvent, Message, Bot, MessageSegment
from nonebot.params import CommandArg
from nonebot_plugin_apscheduler import scheduler

from configs.config import Config
from ..core.database import UserSanityModel

sanity_notify_interval = Config.get_config("zhenxun_arktools", "SANITY_NOTIFY_INTERVAL")
sanity_notify_switch = Config.get_config("zhenxun_arktools", "SANITY_NOTIFY_SWITCH")

add_notify = on_command("理智提醒", aliases={"ADDSAN"}, block=True)
check_notify = on_command("理智查看", aliases={"CHECKSAN"}, block=True)


@add_notify.handle()
async def _(event: GroupMessageEvent, args: Message = CommandArg()):
    args = args.extract_plain_text().strip().split()
    uid = event.user_id
    gid = event.group_id if isinstance(event, GroupMessageEvent) else 0
    now = datetime.now()

    if not args:
        notify_time = datetime.fromtimestamp(now.timestamp() + 135 * 360, tz=now.tzinfo)
        data = await UserSanityModel.filter(gid=gid, uid=uid).first()
        if not data:
            await UserSanityModel.create(
                gid=gid, uid=uid, record_time=now, notify_time=notify_time, status=1
            )
        else:
            await UserSanityModel.filter(gid=gid, uid=uid).update(
                record_san=0, notify_san=135,
                record_time=now, notify_time=notify_time, status=1
            )
    elif len(args) == 2:
        record_san, notify_san = args
        notify_time = datetime.fromtimestamp(now.timestamp() + (int(notify_san) - int(record_san)) * 360, tz=now.tzinfo)
        data = await UserSanityModel.filter(gid=gid, uid=uid).first()
        if not data:
            await UserSanityModel.create(
                gid=gid, uid=uid, record_san=record_san, notify_san=notify_san,
                record_time=now, notify_time=notify_time, status=1
            )
        else:
            await UserSanityModel.filter(gid=gid, uid=uid).update(
                record_san=record_san, notify_san=notify_san,
                record_time=now, notify_time=notify_time, status=1
            )
    else:
        await add_notify.finish("小笨蛋，命令的格式是：“理智提醒 [当前理智] [回满理智]” 或 “理智提醒” 哦！")

    await add_notify.finish(f"记录成功！将在 {notify_time.__str__()[:-7]} 提醒博士哦！")


@check_notify.handle()
async def _(event: MessageEvent):
    uid = event.user_id
    gid = event.group_id if isinstance(event, GroupMessageEvent) else 0

    data = await UserSanityModel.filter(gid=gid, uid=uid, status=1).first()
    if not data:
        await check_notify.finish("小笨蛋，你还没有记录过理智提醒哦！")

    data = data.__dict__

    record_time: datetime = data["record_time"]
    notify_time: datetime = data["notify_time"]
    now = datetime.now(tz=record_time.tzinfo)

    elapsed_time = now - record_time
    remain_time = notify_time - now

    recoverd_san: int = elapsed_time.seconds // 360 if elapsed_time.seconds >= 360 else 0
    now_san: int = data["record_san"] + recoverd_san

    await check_notify.finish(f"距离理智恢复完毕还有 {remain_time.__str__()[:-7]}，当前理智：{now_san}(+{recoverd_san})")


@scheduler.scheduled_job(
    "interval",
    minutes=sanity_notify_interval,
)
async def _():
    if sanity_notify_switch:
        logger.debug("checking sanity...")
        try:
            bot: Bot = get_bot()
        except ValueError:
            pass
        else:
            now = datetime.now()
            try:
                data = await UserSanityModel.filter(notify_time__lt=now, status=1).all()
            except tortoise.exceptions.BaseORMException:
                logger.error("检查理智提醒失败，数据库未初始化")
            else:
                if data:
                    for model in data:
                        if model.gid:
                            await bot.send_group_msg(
                                group_id=model.gid,
                                message=Message(MessageSegment.at(model.uid) + f"你的理智已经恢复到{model.notify_san}了哦！")
                            )
                        else:
                            await bot.send_private_msg(
                                user_id=model.uid,
                                message=Message(MessageSegment.at(model.uid) + f"你的理智已经恢复到{model.notify_san}了哦！")
                            )
                        await UserSanityModel.filter(gid=model.gid, uid=model.uid).update(status=0)


__zx_plugin_name__ = "理智提醒"
__plugin_usage__ = """
usage:
    在理智回满时@用户提醒
    指令:
        理智提醒 => 默认记当前理智为0，回满到135时提醒
        理智提醒 [当前理智] [回满理智] => 同上，不过手动指定当前理智与回满理智
        理智查看 => 查看距离理智回满还有多久，以及当期理智为多少
""".strip()
__plugin_des__ = "在理智回满时@用户提醒"
__plugin_cmd__ = ["理智提醒", "ADDSAN", "理智查看", "CHECKSAN"]
__plugin_settings__ = {
    "cmd": ["理智提醒", "ADDSAN", "理智查看", "CHECKSAN"]
}
__plugin_type__ = ("方舟相关", 1)
__plugin_version__ = 1.0
__plugin_author__ = "Number_Sir<number_sir@126.com>"
__plugin_task__ = {

}
