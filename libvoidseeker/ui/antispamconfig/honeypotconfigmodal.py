import discord
import discord.ui
from discord.ui import ChannelSelect

from ...data import ServerSettings

from ..base import AutoDeferModal, BooleanSelect, CustomChannelSelect


class HoneypotConfigModal(AutoDeferModal):

    def __init__(self, voidseeker, userId, data: ServerSettings):
        super().__init__(voidseeker, userId, data, title="Configure Honey Pot Channel")

        self.enableSelect = BooleanSelect("Honey Pot Enabled", 0, "Enabled", "Disabled", True)

        selectedChannel = []
        if self.data.honeyPotChannelId != 0:
            selectedChannel.append(self.voidseeker.get_channel(self.data.honeyPotChannelId))

        self.honeyPotChannelSelect = CustomChannelSelect(
            placeholder="Select Honey Pot Channel",
            disabled=False,
            default_values=selectedChannel,
            channel_types=[discord.ChannelType.text],
            required=False,
            row=1)

        self.honeyPotText = discord.ui.TextInput(
            label='Honey Pot Message Text',
            placeholder='Text for the honeypot channel message',
            min_length=0,
            max_length=1000,
            required=False,
            default=self.data.honeyPotChannelText,
            row=2,
            style=discord.TextStyle.paragraph
        )

        self.enableSelectLabel = discord.ui.Label(text="Enable Honey Pot Channel", component=self.enableSelect)
        self.honeyPotSelectLabel = discord.ui.Label(text="Select Honey Pot Channel", component=self.honeyPotChannelSelect)

        self.add_item(self.enableSelectLabel)
        self.add_item(self.honeyPotSelectLabel)
        self.add_item(self.honeyPotText)

    async def honeyPotCallback(self, value):
        self.data.honeyPotChannelEnabled = value

    async def channelCallback(self, values):
        print(values[0])

    async def on_submit(self, interaction: discord.Interaction):

        self.enableSelect.updateSelectedValue()

        self.data.honeyPotChannelEnabled = self.enableSelect.selectedValue
        if self.data.honeyPotChannelEnabled:
            self.data.honeyPotChannelId = self.honeyPotChannelSelect.values[0].id
            self.data.honeyPotChannelText = self.honeyPotText.value

        content = "Test Content, do more later"
        await interaction.response.edit_message(content=content, embed=None, view=None)

        self.stop()
