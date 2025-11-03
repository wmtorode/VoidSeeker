try:
    import discord
except:
    pass

from .serversettings import ServerSettings

class Command:

    def __init__(self, function, helpTxt, restriction=None, channels=None):

        self.fncPointer = function
        self.restriction = restriction
        self.helpTxt = helpTxt
        self.channels = channels

    async def canRunRestrictedCommand(self, message: discord.Message, command, serverSettings: ServerSettings, bMsg=True):
        author = message.author  # type: discord.abc.User
        if self.channels:
            if message.channel.id not in self.channels:
                if bMsg:
                    await message.channel.send("Command not valid in this channel, try another channel")
                return False
        try:
            if command.canRun(author, serverSettings):
                return True
            else:
                if bMsg:
                    await message.channel.send("VoidSeeker does not recognize your authority")
        except:
            if bMsg:
                await message.channel.send("Command not available")
        return False

    async def canAccessHelp(self, message, serverSettings: ServerSettings):
        if self.helpTxt == '':
            return False
        if self.restriction:
            return await self.canRunRestrictedCommand(message, self.restriction, serverSettings, bMsg=False)
        return True

    async def runCommand(self, message: discord.Message, serverSettings: ServerSettings):
        canRun = True
        if self.restriction:
            canRun = await self.canRunRestrictedCommand(message, self.restriction, serverSettings)
        if canRun:
            try:
                await message.channel.typing()
            except:
                pass
            await self.fncPointer(message, serverSettings)
