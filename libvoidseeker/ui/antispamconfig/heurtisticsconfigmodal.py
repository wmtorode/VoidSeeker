import discord
import discord.ui

from ...data import ServerSettings
from ..base import AutoDeferModal, BooleanSelect


class HeuristicsConfigModal(AutoDeferModal):

    def __init__(self, voidseeker, userId, data: ServerSettings):
        super().__init__(voidseeker, userId, data, title="Configure Honey Pot Channel")

        self.enableSelect = BooleanSelect("Anti-Spam Heuristics Enabled", 0, "Enabled", "Disabled", True)

        self.spamTermsText = discord.ui.TextInput(
            label='Spam Terms',
            placeholder='Enter Terms to flag as possible spam, separated by a comma (,)',
            min_length=0,
            max_length=2000,
            required=False,
            default=','.join(self.data.spamTerms),
            row=2,
            style=discord.TextStyle.paragraph
        )

        self.spamUrlsText = discord.ui.TextInput(
            label='Spam Urls',
            placeholder='Enter Urls (or URL like terms) to flag as possible spam, separated by a comma (,)',
            min_length=0,
            max_length=2000,
            required=False,
            default=','.join(self.data.spamUrls),
            row=2,
            style=discord.TextStyle.paragraph
        )

        self.enableSelectLabel = discord.ui.Label(text="Enable Honey Pot Channel", component=self.enableSelect)

        self.add_item(self.enableSelectLabel)
        self.add_item(self.spamTermsText)
        self.add_item(self.spamUrlsText)

    async def on_submit(self, interaction: discord.Interaction):

        self.enableSelect.updateSelectedValue()

        self.data.antiSpamHeuristicsEnabled = self.enableSelect.selectedValue
        if self.data.antiSpamHeuristicsEnabled:
            self.data.spamTerms = self.spamTermsText.value.replace('\n', '').split(',')
            self.data.spamUrls = self.spamUrlsText.value.replace('\n', '').split(',')

        # content = "Test Content, do more later"
        # await interaction.response.edit_message(content=content, embed=None, view=None)

        self.stop()