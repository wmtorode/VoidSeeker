import datetime

import discord

from ..data import Command, ServerSettings
from ..model import BanAction
from .basemodule import BaseModule



class ModModule(BaseModule):

    viewReportCmd = BaseModule.CmdPrefix + "report"

    def registerCommands(self):
        return {
            self.viewReportCmd: Command(self.viewReport, "see the last X ban reports for this server", self.modAuth),
        }


    async def viewReport(self, message: discord.Message, serverSettings: ServerSettings):
        reportsToView = self.getIntValue(message, 10)
        if not reportsToView:
            await message.channel.send("Error: Could not read number of entries to fetch")

        self.startSqlEntry()
        subs = self.db.query(BanAction).filter(BanAction.serverId == serverSettings.serverId).order_by(BanAction.id.desc()).limit(reportsToView).all()
        msg = f'viewing last {reportsToView} entries:\n{"Ban Id":<8}{"  User Name":<34}{"  Created At":^18} {"  Joined At":^18} {"  Banned At":^18} {"User ID":^21}\n'
        for sub in subs:  # type: BanAction
            msg += sub.pStat
        await self.chunkMsgs(msg, message, codeblock=True, chunkedChar="\n")