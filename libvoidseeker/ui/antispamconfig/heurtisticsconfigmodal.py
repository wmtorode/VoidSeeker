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
            default=',\n'.join(self.data.spamTerms),
            row=2,
            style=discord.TextStyle.paragraph
        )

        self.spamUrlsText = discord.ui.TextInput(
            label='Spam Urls',
            placeholder='Enter Urls (or URL like terms) to flag as possible spam, separated by a comma (,)',
            min_length=0,
            max_length=2000,
            required=False,
            default=',\n'.join(self.data.spamUrls),
            row=2,
            style=discord.TextStyle.paragraph
        )

        self.spamBanText = discord.ui.TextInput(
            label='Message on Ban',
            placeholder='The message to place into the channel on a ban occuring',
            min_length=0,
            max_length=2000,
            required=False,
            default=self.data.heuristicsBanMessage,
            row=3,
            style=discord.TextStyle.paragraph
        )

        self.enableSelectLabel = discord.ui.Label(text="Enable Honey Pot Channel", component=self.enableSelect)

        self.add_item(self.enableSelectLabel)
        self.add_item(self.spamTermsText)
        self.add_item(self.spamUrlsText)
        self.add_item(self.spamBanText)

    async def on_submit(self, interaction: discord.Interaction):

        self.enableSelect.updateSelectedValue()

        self.data.antiSpamHeuristicsEnabled = self.enableSelect.selectedValue
        if self.data.antiSpamHeuristicsEnabled:
            self.data.spamTerms = self.spamTermsText.value.replace('\n', '').split(',')
            self.data.spamUrls = self.spamUrlsText.value.replace('\n', '').split(',')
            self.data.heuristicsBanMessage = self.spamBanText.value
        self.stop()