import discord
import discord.ui
import json

from ...data import ServerSettings

from ..base import AutoDeferModal, BooleanSelect, NumberSelect


class OcrConfigModal(AutoDeferModal):

    def __init__(self, voidseeker, userId, data: ServerSettings):
        super().__init__(voidseeker, userId, data, title="Configure OCR (Image to Text) System")

        self.enableSelect = BooleanSelect("OCR Enabled", 0, "Enabled", "Disabled", True)

        self.minImageCountSelect = NumberSelect("Minimum Image Count", 1, 4, 1,
                                                userId=None)

        self.rulesFile = discord.ui.FileUpload(required=True, min_values=1, max_values=1)

        self.enableSelectLabel = discord.ui.Label(text="Enable OCR Scanning", component=self.enableSelect)
        self.imageCountSelectLabel = discord.ui.Label(text="Min Attachments to trigger OCR",
                                                      component=self.minImageCountSelect)
        self.rulesFileLabel = discord.ui.Label(text="OCR Rules File", component=self.rulesFile)

        self.add_item(self.enableSelectLabel)
        self.add_item(self.imageCountSelectLabel)
        self.add_item(self.rulesFileLabel)

    async def on_submit(self, interaction: discord.Interaction):

        rulesData = await self.rulesFile.values[0].read()
        rulesData = rulesData.decode("utf-8")

        rulesJson = json.loads(rulesData)

        print(f"OCR Rules File: {rulesData}")

        if not self.data.loadRules(rulesJson):
            raise Exception("Failed to load OCR rules")

        # modals don't use the view callbacks so we need to manually update the values
        self.enableSelect.updateSelectedValue()
        self.minImageCountSelect.updateSelectedValue()

        print(f"OCR Enabled: {self.enableSelect.selectedValue}")
        print(f"Min Images Before Processing: {self.minImageCountSelect.selectedValue}")
        self.data.ocrEnabled = self.enableSelect.selectedValue
        self.data.ocrImagesBeforeProcessing = self.minImageCountSelect.selectedValue

        self.stop()


