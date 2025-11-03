import discord
import datetime
import traceback

from ..data import ServerSettings, DetectionType
from ..model import ServerSetting, BanAction, HoneyPotChannel

from .basemodule import BaseModule


class SpamModule(BaseModule):


    async def checkIfSpambot(self, message: discord.Message):
        if message.author.id == self.voidseeker.user.id or message.guild is None:
            return False
        serverSettings = self.getSettings(message.guild.id)
        if serverSettings.antiSpamHeuristicsEnabled:
            if self.checkForSpamMessage(message, serverSettings):
                return await self.checkRoleAndBans(message, serverSettings, True, DetectionType.Heuristic)
        if serverSettings.honeyPotChannelEnabled:
            if message.channel.id == serverSettings.honeyPotChannelId:
                self.logger.info("Detected new potential spambot!")
                return await self.checkRoleAndBans(message, serverSettings, False, DetectionType.HoneyPot)
        return False

    def checkForSpamMessage(self, message: discord.Message, serverSettings: ServerSettings):
        content = message.content.lower()
        criteriaMatched = 0
        termsMatched = 0
        massPings = 0
        for term in serverSettings.spamTerms:
            if term in content:
                termsMatched += 1
        if termsMatched >= 1:
            criteriaMatched += 1
            self.logger.info("Matched one or more spam terms!")
        for url in serverSettings.spamUrls:
            if url in content:
                criteriaMatched += 1
                self.logger.info(f"Matched spam url: {url}")
                break
        if '@here' in content or '@everyone' in content:
            criteriaMatched += 1
            if '@here' in content:
                massPings += 1
            if '@everyone' in content:
                massPings += 1
            self.logger.info(f"mention @everyone or @here attempted!")
        if criteriaMatched >= 2 or massPings > 1:
            self.logger.warning(f"Found likely spambot, msg: {content}")
            return True
        return False

    async def checkRoleAndBans(self, message: discord.Message, serverSettings: ServerSettings, msgOnBan, detectionMethod):
        for role in message.author.roles:
            if role.id in serverSettings.antiSpamImmuneRoles:
                self.logger.info(f"User is immune to spambot rules for having role {role.name}")
                await message.delete(delay=3)
                return False
        if message.author.id in serverSettings.serverAdmins or message.author.id in serverSettings.serverModerators or message.author.id in self.voidseeker.ownerIds:
            self.logger.info("User is immune as they are an admin, mod or owner on this server!")
            await message.delete(delay=3)
            return False
        if msgOnBan:
            await message.reply(embed=self.makeInformationalEmbed(serverSettings.heuristicsBanMessage))
        await self.banSpamBot(serverSettings, message, detectionMethod)
        return True

    async def banSpamBot(self, serverSettings: ServerSettings, message: discord.Message, detectionMethod):
        self.startSqlEntry()
        serverSettingDb = self.Session.query(ServerSetting).filter(ServerSetting.serverId == serverSettings.serverId).first() # type: ServerSetting
        serverSettingDb.banCount += 1
        honeyPotChannel = self.Session.query(HoneyPotChannel).filter(HoneyPotChannel.serverId == serverSettings.serverId).first()
        serverSettings.banCount = serverSettingDb.banCount

        banAction = BanAction()
        banAction.serverId = serverSettings.serverId
        banAction.userId = message.author.id
        banAction.userName = message.author.display_name
        banAction.createdAt = message.author.created_at
        banAction.joinedAt = message.author.joined_at
        banAction.bannedAt = datetime.datetime.now(datetime.UTC)
        banAction.detectionMethod = detectionMethod
        banAction.banId = serverSettings.banCount
        self.Session.add(banAction)

        try:
            await message.guild.ban(message.author, reason="likely Spambot detected", delete_message_days=1)
        except:
            self.logger.error("Unable to ban spambot!")
            trace = traceback.format_exc()
            for line in trace.split('\n'):
                self.logger.error(line)
            self.Session.rollback()
            role = message.guild.get_role(serverSettings.antiSpamImmuneRoles[0])
            await message.channel.send(f"{role.mention} unable to ban spam bot, pls help!")
            return

        guild = message.guild
        self.Session.commit()
        await self._updateHoneyPotMessage(guild, serverSettings, honeyPotChannel)
        self.logger.info(f"Banned {message.author.name} for as a spambot!")

    async def _makeHoneyPotMessage(self, guild: discord.Guild, serverSettings: ServerSettings, hpChannel: HoneyPotChannel):
        channel = guild.get_channel(hpChannel.channelId)
        message = await channel.send(serverSettings.honeyPotChannelText.format(serverSettings.banCount))
        hpChannel.messageId = message.id

    async def _updateHoneyPotMessage(self, guild: discord.Guild, serverSettings: ServerSettings, hpChannel: HoneyPotChannel):
        if hpChannel:
            channel = guild.get_channel(hpChannel.channelId)
            try:
                message = await channel.fetch_message(hpChannel.messageId)
                await message.edit(content=serverSettings.honeyPotChannelText.format(serverSettings.banCount))
            except:
                self.logger.critical("HoneyPot Message update failure!")
                trace = traceback.format_exc()
                for line in trace.split('\n'):
                    self.logger.error(line)

    async def initHoneyPotChannel(self, serverSettings: ServerSettings):
        if serverSettings.honeyPotChannelEnabled:
            hpChannel = self.Session.query(HoneyPotChannel).filter(HoneyPotChannel.serverId == serverSettings.serverId).first()
            if not hpChannel:
                hpChannel = HoneyPotChannel()
                hpChannel.serverId = serverSettings.serverId
                hpChannel.channelId = 0
                self.Session.add(hpChannel)
            guild = self.voidseeker.get_guild(serverSettings.serverId)
            if serverSettings.honeyPotChannelId != hpChannel.channelId:
                hpChannel.channelId = serverSettings.honeyPotChannelId
                await self._makeHoneyPotMessage(guild, serverSettings, hpChannel)
            else:
                channel = self.voidseeker.get_channel(hpChannel.channelId)
                try:
                    message = await channel.fetch_message(hpChannel.messageId)
                    expectedText = serverSettings.honeyPotChannelText.format(serverSettings.banCount)
                    if message.content.lower() != expectedText.lower():
                        await self._updateHoneyPotMessage(guild, serverSettings, hpChannel)
                except:
                    await self._makeHoneyPotMessage(guild, serverSettings, hpChannel)


    async def initHoneyPots(self):
        self.startSqlEntry()
        for setting in self.settings.serverSettings.values():
            await self.initHoneyPotChannel(setting)
        self.Session.commit()