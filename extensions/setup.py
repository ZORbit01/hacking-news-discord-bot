import lightbulb
import hikari
from lightbulb.utils import pag, nav
from hikari.permissions import Permissions
from database.models import Subscription


set_channel = lightbulb.Plugin("setup channel", "choose channel to send the data into")

set_channel.add_checks(
    lightbulb.checks.has_guild_permissions(hikari.Permissions.ADMINISTRATOR),
    lightbulb.checks.bot_has_guild_permissions(hikari.Permissions.ADMINISTRATOR),
    lightbulb.guild_only,
)


@set_channel.command()
@lightbulb.option("channel", "channel where message to be sent", hikari.TextableChannel)
@lightbulb.option("image_url", "image to be sent", str, required=False, default=None)
@lightbulb.app_command_permissions(hikari.Permissions.ADMINISTRATOR, dm_enabled=False)
@lightbulb.command("setchannel", "set news channel", auto_defer=True,pass_options=True)
@lightbulb.implements(lightbulb.SlashCommand)
async def set_channels(
    ctx: lightbulb.Context, channel: hikari.channels.GuildTextChannel, image_url: str
):
    server_id = ctx.get_guild().id
    user_id = ctx.author.id
    channel_id = int(channel)
    sub = Subscription(
        server_id=server_id,
        user_setter_id=user_id,
        channel_id=channel,
        image_url=image_url,
    )
    if await Subscription.exists(server_id=server_id):
        subs = await Subscription.get(server_id=server_id)
        subs.channel_id = channel_id
        subs.image_url = image_url
        subs.user_setter_id = user_id
        await subs.save()
        
    else:
        subs = Subscription(
            server_id=server_id,
            user_setter_id=user_id,
            channel_id=channel_id,
            image_url=image_url,
        )
        await subs.save()

    await ctx.respond(
        f"channel <#{channel_id}> is set to be news channel !", delete_after=5
    )


def load(bot):
    bot.add_plugin(set_channel)


def unload(bot):
    bot.remove_plugin(set_channel)
