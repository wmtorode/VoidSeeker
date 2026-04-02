from .base import ModelBase
from sqlalchemy import Column, String, Integer, Boolean, Text, BigInteger, ForeignKey, Float, JSON, DateTime, Unicode
import datetime


class OcrResult(ModelBase):
    """

    """
    __tablename__ = "ocrResults"
    id = Column(Integer, index=True, primary_key=True)
    serverId = Column(BigInteger, default=0, index=True)
    userId = Column(BigInteger, default=0)
    addedAt = Column(DateTime, default=datetime.datetime.now(datetime.UTC))
    ocrResultJson = Column(JSON, default={})
    historic = Column(Boolean, default=False)
    rulesBreached = Column(Text, default="")
    channelId = Column(BigInteger, default=0)

    def _renderList(self, prop):
        if len(prop) == 1:
            return prop[0]
        stMsg = ''
        for item in prop:
            stMsg += f'- {item}\n'
        return stMsg

    @property
    def rulesDetections(self):
        return self._renderList(self.rulesBreached.split(';'))