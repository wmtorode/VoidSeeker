import discord
import discord.ui

from ..base import NavButton, AutoDeferView
from ...data import ServerSettings

from .honeypotconfigmodal import HoneypotConfigModal
from .heurtisticsconfigmodal import HeuristicsConfigModal
from .immunerolesmodal import ImmuneRolesConfigModal


class StartSpamConfigView(AutoDeferView):

    def __init__(self, voidseeker, userId, data: ServerSettings):
        super().__init__(voidseeker, userId, data)

        self.honeyPotButton = NavButton(discord.ButtonStyle.blurple, "Configure Honey Pot Channel", 0, modal=HoneypotConfigModal)
        self.heuristicsButton = NavButton(discord.ButtonStyle.blurple, "Configure Anti-Spam Heuristics", 0, modal=HeuristicsConfigModal)
        self.immuneRolesButton = NavButton(discord.ButtonStyle.blurple, "Configure Role Immunity", 0, modal=ImmuneRolesConfigModal)


        self.commitButton = NavButton(discord.ButtonStyle.green, "Commit Changes", 1,
                                      embed=self.voidseeker.baseModule.makeInformationalEmbed("Config Saved"),
                                      bEnd=True, viewCallback=self.commitCallback)
        self.doneButton = NavButton(discord.ButtonStyle.red, "Cancel", 1,
                                    embed=self.voidseeker.baseModule.makeInformationalEmbed("Config Cancelled"),
                                    bEnd=True, viewCallback=self.cancelCallback)

        self.add_item(self.honeyPotButton)
        self.add_item(self.heuristicsButton)
        self.add_item(self.immuneRolesButton)
        self.add_item(self.commitButton)
        self.add_item(self.doneButton)

    async def commitCallback(self):
        await self.voidseeker.adminModule.persistServerSettings(self.userId, self.data)
        self.voidseeker.rebuildServerSettings(self.data)
        await self.voidseeker.spamModule.initHoneyPotChannel(self.voidseeker.spamModule.getSettings(self.data.serverId))
        self.voidseeker.Session.commit()

        return True

    async def cancelCallback(self):
        self.voidseeker.rebuildServerSettings(self.data)
        return True
