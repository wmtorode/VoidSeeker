import discord


class NumberSelect(discord.ui.Select):

    def __init__(self, placeholderText, startIndex, endIndex, row, displayOffset=0, userId=None, viewCallback=None):

        self.startIndex = startIndex
        self.endIndex = endIndex
        self.selectedValue = -1
        self.userId = userId
        self.viewCallback = viewCallback

        options = []

        num = self.startIndex
        while num <= endIndex:
            options.append(discord.SelectOption(label=str(num + displayOffset), description=str(num + displayOffset),
                                                value=str(num)))
            num += 1

        super().__init__(placeholder=placeholderText, min_values=1, max_values=1, options=options, row=row)

    async def callbackInternal(self):
        self.selectedValue = int(self.values[0])
        if self.viewCallback:
            await self.viewCallback(self.selectedValue)

    async def callback(self, interaction: discord.Interaction):
        if self.userId:
            if self.userId == interaction.user.id:
                await self.callbackInternal()
        else:
            await self.callbackInternal()