import discord
import discord.ui

from ...data import ServerSettings

from ..base import AutoDeferModal, BooleanSelect, CustomChannelSelect


class WelcomeLogConfigModal(AutoDeferModal):

    def __init__(self, voidseeker, userId, data: ServerSettings):
        super().__init__(voidseeker, userId, data, title="Configure Welcome log")

        self.enableSelect = BooleanSelect("Welcome Log Enabled?", 0, "Enabled", "Disabled", True)

        selectedChannel = []
        if self.data.welcomeCheckChannelId != 0:
            selectedChannel.append(self.voidseeker.get_channel(self.data.welcomeCheckChannelId))

        self.welcomeLogChannelSelect = CustomChannelSelect(
            placeholder="Select Welcome Log Channel",
            disabled=False,
            default_values=selectedChannel,
            channel_types=[discord.ChannelType.text],
            required=False,
            row=1)

        self.enableSelectLabel = discord.ui.Label(text="Enable Welcome Log", component=self.enableSelect)
        self.welcomeSelectLabel = discord.ui.Label(text="Select Welcome Log Channel", component=self.welcomeLogChannelSelect)

        self.add_item(self.enableSelectLabel)
        self.add_item(self.welcomeSelectLabel)


    async def on_submit(self, interaction: discord.Interaction):

        self.enableSelect.updateSelectedValue()

        self.data.welcomeCheckEnabled = self.enableSelect.selectedValue
        if self.data.welcomeCheckEnabled:
            self.data.welcomeCheckChannelId = self.welcomeLogChannelSelect.values[0].id

        self.stop()
