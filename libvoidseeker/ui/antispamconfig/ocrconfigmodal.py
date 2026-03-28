import discord
import discord.ui

from ...data import ServerSettings

from ..base import AutoDeferModal, BooleanSelect, NumberSelect


class OcrConfigModal(AutoDeferModal):

    def __init__(self, voidseeker, userId, data: ServerSettings):
        super().__init__(voidseeker, userId, data, title="Configure OCR (Image to Text) System")

        self.enableSelect = BooleanSelect("OCR Enabled", 0, "Enabled", "Disabled", True)

        self.minImageCountSelect = NumberSelect("Minimum Image Count", 1, 4, 1, viewCallback=self.imagesCallback)

        self.enableSelectLabel = discord.ui.Label(text="Enable OCR Scanning", component=self.enableSelect)
        self.imageCountSelectLabel = discord.ui.Label(text="Min Attachments to trigger OCR", component=self.minImageCountSelect)

        self.add_item(self.enableSelectLabel)
        self.add_item(self.imageCountSelectLabel)

    async def on_submit(self, interaction: discord.Interaction):

        self.enableSelect.updateSelectedValue()

        self.data.ocrEnabled = self.enableSelect.selectedValue

        self.stop()

    async def imagesCallback(self, value):
        self.data.ocrImagesBeforeProcessing = value
