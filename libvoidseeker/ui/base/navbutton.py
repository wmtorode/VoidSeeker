import discord


class NavButton(discord.ui.Button):

    ViewCallbackFailedErrorMsg = "View Callback failure, check fields are all valid"

    def __init__(self, style, label, row, embed=None, view=None, content=None, bEnd=False, viewCallback=None, modal=None, afterModalCallback=None):
        super(NavButton, self).__init__(style=style, label=label, row=row)
        self.callbackView = view
        self.embed = embed
        self.content=content
        self.endOnCallback = bEnd
        self.viewCallback = viewCallback
        self.modal = modal
        self.afterModalCallback = afterModalCallback


    def callBackBuilder(self):
        return self.callbackView(self.view.voidseeker, self.view.userId, self.view.data)

    def modalBuilder(self):
        return self.modal(self.view.voidseeker, self.view.userId, self.view.data)

    async def callback(self, interaction: discord.Interaction):
        if interaction.user.id == self.view.userId:

            if self.viewCallback:
                if not await self.viewCallback():
                    await interaction.response.send_message(self.view.voidseeker.baseModule.makeErrorEmbed(self.ViewCallbackFailedErrorMsg))
                    return

            if self.modal:
                modal = self.modalBuilder()
                await interaction.response.send_modal(modal)

                if self.afterModalCallback:
                    await self.afterModalCallback(interaction)

            else:
                view = None
                if self.callbackView:
                    view = self.callBackBuilder()

                await interaction.response.edit_message(content=self.content,
                                                        embed=self.embed,
                                                        view=view)
            if self.endOnCallback:
                self.view.stop()