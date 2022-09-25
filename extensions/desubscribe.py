import lightbulb
import hikari
from lightbulb.utils import pag, nav
from hikari.permissions import Permissions
from database.models import Subscription


unset_channel = lightbulb.Plugin(
    "setup channel", "choose channel to send the data into"
)

unset_channel.add_checks(
    lightbulb.checks.has_guild_permissions(hikari.Permissions.ADMINISTRATOR),
    lightbulb.checks.bot_has_guild_permissions(hikari.Permissions.ADMINISTRATOR),
    lightbulb.guild_only,
)


@unset_channel.command()
@lightbulb.app_command_permissions(hikari.Permissions.ADMINISTRATOR, dm_enabled=False)
@lightbulb.command("unset", "unset news channel", auto_defer=True, pass_options=True)
@lightbulb.implements(lightbulb.SlashCommand)
async def unset_channels(ctx: lightbulb.Context):
    server_id = ctx.get_guild().id
    if await Subscription.exists(server_id=server_id):
        subs = await Subscription.get(server_id=server_id)
        await subs.delete()
    else:
        await ctx.respond(f"you didn't set channel yet", delete_after=5)
    await ctx.respond("channel is unset from beign news channel!", delete_after=5)


def load(bot):
    bot.add_plugin(unset_channel)


def unload(bot):
    bot.remove_plugin(unset_channel)
