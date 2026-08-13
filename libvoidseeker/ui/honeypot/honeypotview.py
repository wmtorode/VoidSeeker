from discord.ui import LayoutView, Container, TextDisplay, Section, Thumbnail

from ...data import ServerSettings


class HoneypotView(LayoutView):

    def __init__(self, serverSettings: ServerSettings, iconUrl):
        super().__init__(timeout=None)

        self.container = Container(
            Section(
                TextDisplay(serverSettings.honeyPotChannelText.format(serverSettings.banCount)),
                accessory=Thumbnail(iconUrl)
            )
        )

        self.add_item(self.container)