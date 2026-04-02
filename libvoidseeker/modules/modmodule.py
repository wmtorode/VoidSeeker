import discord

from .. import OCRData, OcrResult
from ..data import Command, ServerSettings
from ..model import BanAction
from .basemodule import BaseModule


class ModModule(BaseModule):

    viewReportCmd = BaseModule.CmdPrefix + "report"
    banDetailsCmd = BaseModule.CmdPrefix + "details"
    ocrRecallCmd = BaseModule.CmdPrefix + "review"

    def registerCommands(self):
        return {
            self.viewReportCmd: Command(self.viewReport, "see the last X ban reports for this server", self.modAuth),
            self.banDetailsCmd: Command(self.banDetails, "see the details of a ban (specify ban ID)", self.modAuth),
            self.ocrRecallCmd: Command(self.ocrRecall, "recall the images that lead to an OCR ban (specify ban ID)",
                                       self.modAuth)
        }

    async def viewReport(self, message: discord.Message, serverSettings: ServerSettings):
        reportsToView = self.getIntValue(message, 10)
        if not reportsToView:
            await message.channel.send("Error: Could not read number of entries to fetch")

        self.startSqlEntry()
        subs = self.Session.query(BanAction).filter(BanAction.serverId == serverSettings.serverId).order_by(BanAction.id.desc()).limit(reportsToView).all()
        msg = f'viewing last {reportsToView} entries, use {self.banDetailsCmd} for more details on a particular ban:\n'
        msg += f'{"Ban Id":<8}{"  User Name":<34}{"  Method":<18} {"  Banned At":^18}\n'
        for sub in subs:  # type: BanAction
            msg += sub.pStat
        await self.chunkMsgs(msg, message, codeblock=True, chunkedChar="\n")

    async def ocrRecall(self, message: discord.Message, serverSettings: ServerSettings):
        banId = self.getIntValue(message, 0)
        if not banId:
            banId = serverSettings.banCount

        self.startSqlEntry()
        ban = self.Session.query(BanAction).filter(BanAction.serverId == serverSettings.serverId,
                                                   BanAction.banId == banId).first()
        if not ban:
            await message.channel.send(embed=self.makeErrorEmbed("Could not find ban with that ID"))
            return
        ocrResult = self.Session.query(OcrResult).filter(OcrResult.id == ban.ocrResultId).first()
        if not ocrResult:
            await message.channel.send(embed=self.makeInformationalEmbed("Could not find OCR result for this ban"))
            return
        await message.channel.send("Recalling Images that lead to ban")
        ocrData = OCRData()
        ocrData.fromJson(ocrResult.ocrResultJson)
        for image in ocrData.images:
            await self.sendFile(f"ocr/{image}", message.channel)

    async def banDetails(self, message: discord.Message, serverSettings: ServerSettings):
        banId = self.getIntValue(message, 0)
        if not banId:
            banId = serverSettings.banCount

        self.startSqlEntry()
        ban = self.Session.query(BanAction).filter(BanAction.serverId == serverSettings.serverId,
                                                   BanAction.banId == banId).first()  # type: BanAction
        ocrResult = None

        if not ban:
            await message.channel.send(embed=self.makeErrorEmbed("Could not find ban with that ID"))
            return

        if ban.ocrResultId:
            ocrResult = self.Session.query(OcrResult).filter(OcrResult.id == ban.ocrResultId).first()

        embed = discord.Embed(title=f"Ban #{ban.banId}", colour=discord.Colour.magenta(),
                              description="Detailed Ban Report")
        embed.set_author(name=self.user.display_name, icon_url=self.user.display_avatar.url)

        embed.add_field(name="User ID", value=str(ban.userId), inline=True)
        embed.add_field(name="User Name", value=ban.userName, inline=True)
        embed.add_field(name="Detection Method", value=ban.detectionMethod, inline=False)
        embed.add_field(name="Ban ID", value=str(ban.banId), inline=True)
        embed.add_field(name="Account Created At", value=ban.createdAt.isoformat(sep=" ", timespec="minutes"),
                        inline=False)
        embed.add_field(name="Joined Server At", value=ban.joinedAt.isoformat(sep=" ", timespec="minutes"), inline=True)
        embed.add_field(name="Ban Date", value=ban.bannedAt.isoformat(sep=" ", timespec="minutes"), inline=True)

        if ocrResult:
            embed.add_field(name="OCR Results", value=ocrResult.rulesDetections, inline=False)

        embed.set_footer(text=f"{self.user.display_name} Detailed Ban Report", icon_url=self.user.display_avatar.url)

        await message.channel.send(embed=embed)
