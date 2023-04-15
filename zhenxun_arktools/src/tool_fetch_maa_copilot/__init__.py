"""从 https://prts.plus 获取自动作业数据"""
from nonebot import on_command, get_bot, logger
from nonebot.adapters.onebot.v11 import GroupMessageEvent, Message, Bot, MessageSegment
from nonebot.params import CommandArg
from nonebot_plugin_apscheduler import scheduler

from .data_source import (
    add_maa_sub,
    del_maa_sub,
    que_maa_sub,
    fetch_works,
    SubManager,
    process_works,
    process_copilot_data,
    build_result_image,
    DEFAULT_PARAMS,
    ORDERS
)
from configs.config import Config
from ..exceptions import MAAFailedResponseException, MAANoResultException

query_copilot = on_command("maa查作业", aliases={"maa抄作业"})
add_sub = on_command("maa添加订阅", aliases={"ADDMAA"})
del_sub = on_command("maa删除订阅", aliases={"DELMAA"})
get_sub = on_command("maa查看订阅", aliases={"GETMAA"})


maa_copilot_interval = Config.get_config("zhenxun_arktools", "MAA_COPILOT_INTERVAL")
maa_copilot_switch = Config.get_config("zhenxun_arktools", "MAA_COPILOT_SWITCH")

sub_manager = SubManager()


@query_copilot.handle()
async def _(args: Message = CommandArg()):
    keywords = args.extract_plain_text().strip()
    if not keywords:
        await add_sub.finish()

    keywords = keywords.split("|")
    if len(keywords) == 1:
        keywords, order_by = keywords[0], ORDERS["最新"]
    elif len(keywords) == 2:
        keywords, order_by = keywords[0], ORDERS.get(keywords[1], ORDERS["最新"])
    else:
        await query_copilot.finish("输入格式错误！正确的输入格式为:\nmaa查作业 关键词1 关键词2 ...\nmaa查作业 关键词1 关键词2 ... | 热度/最新/访问")

    keywords = "+".join(sorted(set(keywords.split())))
    params = DEFAULT_PARAMS.copy()
    params["document"] = keywords
    params["order_by"] = order_by
    try:
        result = await fetch_works(params)
    except (MAANoResultException, MAAFailedResponseException) as e:
        await query_copilot.finish(e.msg)

    title, details, stage, operators_str = await process_copilot_data(result[0])
    img_bytes = await build_result_image(title, details, stage, operators_str)
    await query_copilot.finish(
        Message(
            MessageSegment.image(img_bytes)) +
            f"查询结果: \n\n关键词: \n{', '.join(keywords.split('+'))}\n\n作业代码: \nmaa://{result[0]['id']}"
    )


@add_sub.handle()
async def _(event: GroupMessageEvent, args: Message = CommandArg()):
    group_id = str(event.group_id)
    keywords = args.extract_plain_text().strip()
    if not keywords:
        await add_sub.finish()

    keywords = "+".join(sorted(set(keywords.split())))
    result = await add_maa_sub(group_id, keywords)
    await add_sub.finish(result)


@del_sub.handle()
async def _(event: GroupMessageEvent, args: Message = CommandArg()):
    group_id = str(event.group_id)
    keywords = args.extract_plain_text().strip()
    if not keywords:
        await del_sub.finish()

    keywords = "+".join(sorted(set(keywords.split())))
    result = await del_maa_sub(group_id, keywords)
    await del_sub.finish(result)


@get_sub.handle()
async def _(event: GroupMessageEvent):
    group_id = str(event.group_id)
    result = await que_maa_sub(group_id)
    await get_sub.finish(result)


@scheduler.scheduled_job(
    "interval",
    minutes=maa_copilot_interval,
)
async def _():
    if maa_copilot_switch:
        global sub_manager
        try:
            bot: Bot = get_bot()
        except ValueError:
            pass
        else:
            try:
                await sub_manager.reload_sub_data()
                for _ in range(len(sub_manager.data)):
                    keyword = await sub_manager.random_sub_data()
                    if keyword:
                        logger.info(f"MAA 作业查询中: {keyword}")
                        params = DEFAULT_PARAMS.copy()
                        params["document"] = keyword
                        try:
                            data = await fetch_works(params)
                        except MAAFailedResponseException as e:
                            logger.error(f"MAA查询作业出错: {e.msg}")
                        except MAANoResultException as e:
                            logger.error(f"MAA查询作业出错: {e.msg}")
                        else:
                            result = await process_works(data, keyword)
                            if result:
                                image, id_, groups = result
                                for group in groups.split():
                                    await bot.send_group_msg(
                                        group_id=int(group),
                                        message=Message(MessageSegment.image(image))
                                                + f"有新的MAA作业: \n\n关键词: \n{', '.join(keyword.split('+'))}\n\n作业代码: \nmaa://{id_}"
                                    )
            except Exception as e:
                logger.error(f"推送 MAA 作业失败！{e}")


__zx_plugin_name__ = "MAA 抄作业"
__plugin_usage__ = """
usage:
    按关键词订阅 MAA 的作业站作业，订阅指定关键词的作业
    指令:
        maa查作业 [关键词1 关键词2 ...] => 按关键词组合查作业，默认为最新发布的第一个作业
        maa查作业 [关键词1 关键词2 ...] | [热度/最新/访问] => 同上，不过可以指定按什么顺序查询
        maa添加订阅 [关键词1 关键词2 ...] => 按关键词组合订阅作业
        maa删除订阅 [关键词1 关键词2 ...] => 删除本群对这些关键词组合的订阅
        maa查看订阅 => 查看本群订阅的所有关键词组合
""".strip()
__plugin_des__ = "在理智回满时@用户提醒"
__plugin_cmd__ = ["maa添加订阅", "ADDMAA", "maa删除订阅", "DELMAA", "maa查看订阅", "GETMAA", "maa查作业"]
__plugin_settings__ = {
    "cmd": ["maa添加订阅", "ADDMAA", "maa删除订阅", "DELMAA", "maa查看订阅", "GETMAA", "maa查作业"]
}
__plugin_type__ = ("方舟相关", 1)
__plugin_version__ = 1.0
__plugin_author__ = "Number_Sir<number_sir@126.com>"
__plugin_task__ = {

}
