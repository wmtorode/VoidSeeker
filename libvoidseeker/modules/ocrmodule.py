import discord
import time

from io import BytesIO

import uuid
import PIL
import pytesseract

from .basemodule import BaseModule
from .. import ServerSettings, OCRData, OcrRequest
from ..data import Command


class OCRModule(BaseModule):

    ocrScanImageCmd = BaseModule.CmdPrefix + 'ocr'

    def registerCommands(self):
        return {
            self.ocrScanImageCmd: Command(self.ocrScanImage, "Scan an Image with OCR and see the results", self.ownerAuth)

        }

    async def ocrScanImage(self, message: discord.Message, serverSettings: ServerSettings):
        if len(message.attachments) >= 1:
            bio = BytesIO(await message.attachments[0].read())
            text = pytesseract.image_to_string(PIL.Image.open(bio))
            self.logger.info(text)
            await message.channel.send(text)
        else:
            await message.channel.send(embed=self.makeErrorEmbed("No image attached"))

    async def processForOcr(self, message: discord.Message):
        serverSettings = self.getSettings(message.guild.id)
        if serverSettings.ocrEnabled and len(message.attachments) >= serverSettings.ocrImagesBeforeProcessing:
            ocrData = OCRData()
            imageCount = 0
            for attachment in message.attachments:
                if self._isImage(attachment):
                    imageCount += 1
            if imageCount >= serverSettings.ocrImagesBeforeProcessing:
                for attachment in message.attachments:
                    if self._isImage(attachment):
                        imageCount += 1
                        id = str(uuid.uuid4())
                        await attachment.save(f"{self.storeDir}/ocr/{id}")
                        ocrData.images.append(id)
                self.startSqlEntry()
                request = OcrRequest()
                request.serverId = message.guild.id
                request.userId = message.author.id
                request.requestJson = ocrData.toJson()
                self.Session.add(request)
                self.Session.commit()
                self.logger.info(f"OCR Request placed")


    def _isImage(self, attachment: discord.Attachment):
        return attachment.content_type.startswith("image/")