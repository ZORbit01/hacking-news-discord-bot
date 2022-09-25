import hikari
import lightbulb
import os
from tortoise import run_async, Tortoise
from database.config import TORTOISE_ORM
from lightbulb.ext import tasks
from hackernews import Item
from utils.const import (
    INTENTS,
    TOKEN,
)

bot = lightbulb.BotApp(
    TOKEN,
    intents=INTENTS,
)
from utils.struct import HackerNewsPrev
from utils.dispatcher import dispatch_message
from tortoise import run_async
hn = HackerNewsPrev()

tasks.load(bot)
run_async(Tortoise.init(config=TORTOISE_ORM))

@bot.listen()
async def on_start(event: hikari.StartedEvent):
    """when bot start"""


@bot.listen()
async def on_stopping(event: hikari.StoppingEvent):
    """when bot shutdown"""
    await Tortoise.close_connections()


bot.load_extensions_from("./extensions/", must_exist=True, recursive=True)


@tasks.task(s=10, auto_start=True)
async def get_news_every_10_seconds():
    await Tortoise.init(config=TORTOISE_ORM)
    news_id = hn.get_latest_news()
    if news_id != hn.prev_news:
        hn.prev_news = news_id
        item = hn.item(news_id)
        await dispatch_message(bot, item)


@bot.listen(lightbulb.CommandErrorEvent)
async def on_error(event):
    if isinstance(event.exception, lightbulb.MissingRequiredPermission):
        await event.context.respond(
            "Unable to excute this command, maybe you don't have permissions",
            reply=True,
            delete_after=5,
        )
        return True
    if isinstance(event.exception, lightbulb.NotEnoughArguments):
        await event.context.respond(
            "Error please check command arguments", reply=True, delete_after=5
        )
        return True
    if isinstance(event.exception, lightbulb.CommandInvocationError):
        await event.context.respond(
            "Command invocation error", reply=True, delete_after=5
        )
        raise event.exception


bot.run()
