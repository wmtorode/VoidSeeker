import discord


class BooleanSelect(discord.ui.Select):

    def __init__(self, placeholderText, row, userId=None, viewCallback=None, TrueLabel=None, FalseLabel=None, required=False):

        self.trueLabel = "True" if TrueLabel is None else TrueLabel
        self.falseLabel = "False" if FalseLabel is None else FalseLabel

        self.selectedValue = False
        self.userId = userId
        self.viewCallback = viewCallback

        options = [
            discord.SelectOption(label=self.trueLabel, description=self.trueLabel, value="1"),
            discord.SelectOption(label=self.falseLabel, description=self.falseLabel, value="0")
        ]

        super().__init__(placeholder=placeholderText, min_values=1, max_values=1, options=options, row=row, required=required)

    async def callbackInternal(self):
        self.updateSelectedValue()
        if self.viewCallback:
            await self.viewCallback(self.selectedValue)

    def updateSelectedValue(self):
        value = int(self.values[0])
        self.selectedValue = value >= 1

    async def callback(self, interaction: discord.Interaction):
        if self.userId:
            if self.userId == interaction.user.id:
                await self.callbackInternal()
        else:
            await self.callbackInternal()