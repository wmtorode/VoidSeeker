import discord


from ..data import ServerSettings, Command
from .basemodule import BaseModule

class TestModule(BaseModule):

    getUserMsgCountCmd = BaseModule.CmdPrefix + 'msgCount'

    def registerCommands(self):
        return {
            self.getUserMsgCountCmd: Command(self.getUserMsgCount, "Test command", self.ownerAuth),
        }

    async def getUserMsgCount(self, message: discord.Message, serverSettings: ServerSettings):
        guild = message.guild
        for mention in message.mentions:
            member = await guild.fetch_member(mention.id)
            msgCount = 0
            async for msg in member.history():
                msgCount += 1

            await message.channel.send(f"{member.display_name}'s message count is {msgCount}")
