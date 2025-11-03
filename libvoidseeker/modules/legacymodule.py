import discord
import json
import datetime

from ..data import ServerSettings, Command, DetectionType
from ..model import ServerSetting, BanAction
from .basemodule import BaseModule


class LegacyModule(BaseModule):


    importFromRbCmd = BaseModule.NativeCommandPrefix + "rbimport"

    def registerCommands(self):
        return {
            self.importFromRbCmd: Command(self.importFromRb, "Import Historic Data from RogueBot", self.ownerAuth),
        }

    # Import Legacy Data from our previous bot that handled this system
    async def importFromRb(self, message: discord.Message, serverSettings: ServerSettings):

        if len(message.attachments) >= 1:
            await message.channel.send(embed=self.makeInformationalEmbed("Importing Historic Data"))
            data = await message.attachments[0].read()

            Jdata = json.loads(data)
            servers = {}

            self.startSqlEntry()
            for channel in Jdata["OFChannels"]:

                serverId = channel["serverId"]
                serverSettingDb = self.Session.query(ServerSetting).filter(ServerSetting.serverId == serverId).first()
                if not serverSettingDb:
                    serverSettingDb = ServerSetting()
                    serverSettingDb.serverId = serverId
                    serverSettingDb.banCount = 0

                servers[serverId] = serverSettingDb

            for historicBan in Jdata["OFSubs"]:

                bannedFromServer = historicBan["serverId"]
                ban = BanAction()
                ban.serverId = bannedFromServer
                ban.userId = historicBan["userId"]
                ban.userName = historicBan["userName"]
                ban.bannedAt = datetime.datetime.fromisoformat(historicBan["bannedAt"])
                ban.createdAt = datetime.datetime.fromisoformat(historicBan["createdAt"])
                ban.joinedAt = datetime.datetime.fromisoformat(historicBan["joinedAt"])
                ban.detectionMethod = DetectionType.Unknown
                servers[bannedFromServer].banCount += 1
                ban.banId = servers[bannedFromServer].banCount
                self.Session.add(ban)

            for server in servers.values():
                self.Session.add(server)

            self.Session.commit()

        self.voidseeker.initSettings()
        await message.channel.send(embed=self.makeSuccessEmbed("Imported Historic Data"))
        await message.delete(delay=2)




