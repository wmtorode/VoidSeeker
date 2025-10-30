import discord
import discord.ui

from ..base import NavButton, AutoDeferView
from ...data import ServerSettings

from .honeypotconfigmodal import HoneypotConfigModal


class StartSpamConfigView(AutoDeferView):

    def __init__(self, voidseeker, userId, data: ServerSettings):
        super().__init__(voidseeker, userId, data)

        self.honeyPotButton = NavButton(discord.ButtonStyle.green, "Configure Honey Pot Channel", 0, modal=HoneypotConfigModal)
        self.doneButton = NavButton(discord.ButtonStyle.red, "Cancel", 0,
                                    embed=self.voidseeker.baseModule.makeInformationalEmbed("Config Cancelled"),
                                    bEnd=True)

        self.add_item(self.honeyPotButton)
        self.add_item(self.doneButton)