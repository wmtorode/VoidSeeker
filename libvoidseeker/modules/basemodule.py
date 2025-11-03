import discord
import json
import logging
import os
import os.path
import time
import traceback
from io import BytesIO

from .. import ServerSetting
from ..data import BotSettings, CommandAuth, ServerSettings

TEST_MODE = os.getenv("TEST_MODE", default="No")


class BaseModule:

    CmdPrefix = "!vs"
    CollidingPrefix = "$vs"
    NativeCommandPrefix = "&vs"
    if TEST_MODE.lower() == "yes":
        CmdPrefix = "vs!"
        CollidingPrefix = "vs$"
        NativeCommandPrefix = "vs&"

    def __init__(self, logger: logging.Logger, settings: BotSettings, dbSession, voidseeker: discord.Client, storeDir):
        self.logger = logger
        self.settings = settings
        self.Session = dbSession
        self.voidseeker = voidseeker
        self.storeDir = storeDir
        self.ownerAuth = CommandAuth(self.voidseeker.ownerIds, True, False, False)
        self.adminAuth = CommandAuth(self.voidseeker.ownerIds, True, True, False)
        self.modAuth = CommandAuth(self.voidseeker.ownerIds, True, True, True)
        self.isInTestMode = TEST_MODE.lower() == "yes"



    @property
    def user(self):
        return self.voidseeker.user

    def registerCommands(self):
        return {}

    def getSettings(self, serverId):
        if serverId in self.settings.serverSettings:
            return self.settings.serverSettings[serverId]
        else:
            return ServerSettings(serverId)

    def logTrace(self):
        self.logger.error('Exception!')
        for line in traceback.format_exc().split("\n"):
            self.logger.error(line)

    def parseMsg(self, message: discord.Message):
        ltMsg = message.content.split()
        if len( ltMsg) == 2:
            stArg = ltMsg[1].strip('\n')

            return stArg
        elif len(ltMsg) > 2:
            return ltMsg[1:]
        else:
            return None

    def getIntValue(self, message, default=10):
        iValue = default
        sValue = self.parseMsg(message)
        if sValue:
            try:
                iValue = int(sValue)
            except:
                return

        return iValue

    async def chunkMsgs(self, stMsg, message: discord.Message, codeblock, chunkedChar=None):
        breakChar = ' '
        if chunkedChar:
            breakChar = chunkedChar
        if len(stMsg) >= 1800:
            idx = 1500
            while idx < len(stMsg) and idx < 1800:
                if stMsg[idx] == breakChar:
                    break
                idx += 1
            msg = stMsg[:idx]
            if codeblock:
                msg = msg.replace('```', '')
                msg = f'```{msg}```'
            await message.channel.send(msg)
            time.sleep(0.1)
            await self.chunkMsgs(stMsg[idx:], message, codeblock)
        else:
            msg = stMsg
            if codeblock:
                msg = stMsg.replace('```', '')
                msg = f'```{msg}```'
            await message.channel.send(msg)

    def startSqlEntry(self):
        """
        Make the SQL connection work, MySQL drops connections after long periods of inactivity, in theory SQLAlchemy's
        settings should handle this, but for whatever reason they dont seem to, so screw it and do it this way


        :return:
        :rtype:
        """
        try:
            self.Session.commit()
        except:
            self.Session.rollback()
            self.Session.commit()

    def ensureServerEntry(self, serverSettings: ServerSettings):
        server = self.Session.query(ServerSetting).filter(ServerSetting.serverId == serverSettings.serverId).first()
        if not server:
            server = ServerSetting()
            server.serverId = serverSettings.serverId
            self.Session.add(server)
            self.Session.commit()
        if serverSettings.serverId not in self.settings.serverSettings:
            self.settings.serverSettings[serverSettings.serverId] = serverSettings

    def makeErrorEmbed(self, msg):
        embed = discord.Embed(colour=discord.Colour.brand_red())
        embed.description = msg
        embed.set_footer(text="MRBC", icon_url=self.user.display_avatar.url)
        return embed

    def makeSuccessEmbed(self, msg):
        embed = discord.Embed(colour=discord.Colour.brand_green())
        embed.description = msg
        embed.set_footer(text="MRBC", icon_url=self.user.display_avatar.url)
        return embed

    def makeInformationalEmbed(self, msg):
        embed = discord.Embed(colour=discord.Colour.dark_purple())
        embed.description = msg
        embed.set_footer(text="MRBC", icon_url=self.user.display_avatar.url)
        return embed

    async def sendFile(self, filename, channel, data=None):

        resource = os.path.join(self.storeDir, filename)
        if data:
            bio = BytesIO()
            bio.write(data)
            bio.seek(0)
            dFile = discord.File(bio, filename=filename)
            await channel.send(file=dFile)
            return
        if os.path.exists(resource):
            dFile = discord.File(resource)
            await channel.send(file=dFile)
        else:
            await channel.send("Resource not found!")
