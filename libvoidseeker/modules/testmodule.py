import discord
import logging


from ..data import ServerSettings, Command, BotSettings
from .basemodule import BaseModule
from ..ui import HoneypotView


class TestModule(BaseModule):

    getUserMsgCountCmd = BaseModule.CmdPrefix + 'msgCount'
    testLayoutCmd = BaseModule.CmdPrefix + 'testLayout'

    def __init__(self, logger: logging.Logger, settings: BotSettings, dbSession, voidseeker: discord.Client, storeDir):

        super().__init__(logger, settings, dbSession, voidseeker, storeDir)

        self.testLayoutMsgId = 0
        self.testLayoutChannelId = 0

    def registerCommands(self):
        return {
            self.getUserMsgCountCmd: Command(self.getUserMsgCount, "Test command", self.ownerAuth),
            self.testLayoutCmd: Command(self.postLayoutMessage, "Test command", self.ownerAuth),
        }

    async def getUserMsgCount(self, message: discord.Message, serverSettings: ServerSettings):
        guild = message.guild
        for mention in message.mentions:
            member = await guild.fetch_member(mention.id)
            msgCount = 0
            async for msg in member.history():
                msgCount += 1

            await message.channel.send(f"{member.display_name}'s message count is {msgCount}")

    async def postLayoutMessage(self, message: discord.Message, serverSettings: ServerSettings):
        serverSettings.banCount += 1
        view = HoneypotView(serverSettings, self.voidseeker.user.avatar.url)
        if self.testLayoutMsgId == 0:
            msg = await message.channel.send(view=view)
            self.testLayoutMsgId = msg.id
            self.testLayoutChannelId = message.channel.id
        else:
            channel = message.guild.get_channel(self.testLayoutChannelId)
            viewMessage = await channel.fetch_message(self.testLayoutMsgId)
            await viewMessage.edit(view=view)
