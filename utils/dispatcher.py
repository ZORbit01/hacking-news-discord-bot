from hackernews import HackerNews
import hackernews
from lightbulb.app import BotApp
from database.models import Subscription
import hikari
import lightbulb
from lightbulb.ext import tasks


async def dispatch_message(bot: BotApp, item: hackernews.Item, image_url=None):
    subscriptions = await Subscription.all()
    for sub in subscriptions:
        try:

            title = "```Hacker's! check this ```"
            time = item.time.astimezone()
            url = item.url if hasattr(item, "url") else "https://google.com"
            description = item.title if hasattr(item, "title") else None
            color = 0x00FFFF
            author = item.by if hasattr(item, "by") else "Unknown"
            embd = hikari.Embed(
                title=title,
                timestamp=time,
                url=url,
                description=description,
                color=color,
            )
            embd.add_field("author ", value=author, inline=False)
            embd.set_thumbnail(sub.image_url)
            await bot.rest.create_message(sub.channel_id, embed=embd)
        except Exception as e:
            print(e)
