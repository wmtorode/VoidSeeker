import discord
import time

from .basemodule import BaseModule
from .. import ServerSettings
from ..data import Command


class StatusModule(BaseModule):

    pingCmd = BaseModule.NativeCommandPrefix + "ping"
    helpCmd = BaseModule.NativeCommandPrefix + "help"

    def registerCommands(self):
        return {
            self.pingCmd: Command(self.ping, "Pings the bot"),
            self.helpCmd: Command(self.generateHelpText, "Displays the help menu")
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
