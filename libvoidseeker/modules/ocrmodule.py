from typing import List

import discord
import time
import os
import shutil

from io import BytesIO

import uuid
import PIL
import pytesseract

from libvoidseeker.data.ocrrule import OcrRule
from .basemodule import BaseModule
from .. import ServerSettings, OCRData, OcrRequest, OcrResult
from ..data import Command, DetectionType

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
                        extension = attachment.filename.split('.')[-1]
                        id = str(uuid.uuid4())
                        await attachment.save(f"{self.storeDir}/ocr/{id}.{extension}")
                        ocrData.images.append(f'{id}.{extension}')
                self.startSqlEntry()
                request = OcrRequest()
                request.serverId = message.guild.id
                request.userId = message.author.id
                request.requestJson = ocrData.toJson()
                request.channelId = message.channel.id
                self.Session.add(request)
                self.Session.commit()
                self.logger.info(f"OCR Request placed")

    async def processOcrResults(self):

        self.startSqlEntry()
        ocrResults = self.Session.query(OcrResult).filter(OcrResult.historic == False).all()
        for ocrResult in ocrResults:
            await self._processResult(ocrResult)


    async def _processResult(self, ocrResult: OcrResult):
        serverSettings = self.getSettings(ocrResult.serverId)
        guild = self.voidseeker.get_guild(ocrResult.serverId)
        user = guild.get_member(ocrResult.userId)
        channel = guild.get_channel(ocrResult.channelId)
        triggeredRules = []
        resultData = OCRData()
        resultData.fromJson(ocrResult.ocrResultJson)
        for result in resultData.results:
            for rule in serverSettings.ocrRules: # type: OcrRule
                if rule.check(result):
                    triggeredRules.append(rule.ruleName)
                    self.logger.info(f"OCR Rule triggered: {rule.ruleName}")
        if len(triggeredRules) > 0:
            self.logger.info("OCR Rules triggered, OCR ban in progress")
            ocrResult.historic = True
            ocrResult.rulesBreached = ';'.join(triggeredRules)
            self.startSqlEntry()
            self.Session.add(ocrResult)
            self.Session.commit()
            await self.banUser(serverSettings, user, guild, channel, DetectionType.Ocr, ocrResult.id)
        else:
            # dont keep detections that had nothing
            for image in resultData.images:
                try:
                    os.remove(f"{self.storeDir}/ocr/{image}")
                except:
                    self.logger.warning(f"failed to remove OCR Image: {image}")
            self.startSqlEntry()
            self.Session.delete(ocrResult)
            self.Session.commit()




    def _isImage(self, attachment: discord.Attachment):
        return attachment.content_type.startswith("image/")