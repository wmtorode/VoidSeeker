import discord
import time

from .basemodule import BaseModule
from .. import ServerSettings
from ..data import Command


class StatusModule(BaseModule):

    pingCmd = BaseModule.NativeCommandPrefix + "ping"
    helpCmd = BaseModule.NativeCommandPrefix + "help"
    getConfigCmd = BaseModule.CmdPrefix + "config"

    def registerCommands(self):
        return {
            self.pingCmd: Command(self.ping, "Pings the bot"),
            self.helpCmd: Command(self.generateHelpText, "Displays the help menu"),
            self.getConfigCmd: Command(self.renderSettings, "Displays the current server settings", self.modAuth)

        }

    async def ping(self, message:discord.Message, serverSettings: ServerSettings):
        await message.channel.send("Pong!")

    async def _makeHelpTxt(self, commandList, channel):
        idx = 0
        embed = self.makeInformationalEmbed("Available Commands:")
        for command in commandList:
            embed.add_field(name=f'{command[0]}', value=command[1], inline=False)
            idx += 1
            if idx % 12 == 0:
                await channel.send(embed=embed)
                time.sleep(0.05)
                embed = self.makeInformationalEmbed("Available Commands Continued:")
                idx = 0
        if idx != 0:
            await channel.send(embed=embed)

    async def generateHelpText(self, message, serverSettings: ServerSettings):
        ltHelpCommands = []
        for command in sorted(self.voidseeker.CommandMap.keys()):
            if await self.voidseeker.CommandMap[command].canAccessHelp(message, serverSettings):
                ltHelpCommands.append([command, self.voidseeker.CommandMap[command].helpTxt])
        await self._makeHelpTxt(ltHelpCommands, message.channel)

    async def renderSettings(self, message: discord.Message, serverSettings: ServerSettings):

        embed = discord.Embed(title="Server Config:", colour=discord.Colour.dark_teal(), description="")
        embed.set_author(name=self.user.display_name, icon_url=self.user.display_avatar.url)

        embed.add_field(name="Honey Pot Enabled", value=str(serverSettings.honeyPotChannelEnabled), inline=True)
        embed.add_field(name="Honey Pot Channel ID", value=str(serverSettings.honeyPotChannelId), inline=True)
        embed.add_field(name="Ban when pings everyone", value=str(serverSettings.banOnPingAll), inline=True)
        embed.add_field(name="Anti-Spam Heuristics Enabled", value=str(serverSettings.antiSpamHeuristicsEnabled), inline=True)

        if serverSettings.honeyPotChannelEnabled:
            embed.add_field(name="Honey Pot Channel Text", value=serverSettings.honeyPotChannelText, inline=False)

        embed.add_field(name="Anti-Spam Immune Roles", value=serverSettings.antiSpamImmuneList, inline=False)
        embed.add_field(name="Ban Terms", value=serverSettings.spamTermList, inline=False)
        embed.add_field(name="Ban Urls", value=serverSettings.spamUrlList, inline=False)

        if serverSettings.antiSpamHeuristicsEnabled:
            embed.add_field(name="Heuristics Ban Text", value=serverSettings.heuristicsBanMessage, inline=False)

        embed.add_field(name="Admins", value=serverSettings.adminList, inline=True)
        embed.add_field(name="Moderators", value=serverSettings.modList, inline=True)

        embed.set_footer(text=f"VoidSeeker Config for server: {message.guild.name}", icon_url=self.user.display_avatar.url)

        await message.channel.send(embed=embed)


