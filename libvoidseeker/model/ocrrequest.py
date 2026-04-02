from .base import ModelBase
from sqlalchemy import Column, String, Integer, Boolean, Text, BigInteger, ForeignKey, Float, JSON, DateTime, Unicode
import datetime


class OcrRequest(ModelBase):
    """

    """
    __tablename__ = "ocrRequests"
    id = Column(Integer, index=True, primary_key=True)
    serverId = Column(BigInteger, default=0, index=True)
    userId = Column(BigInteger, default=0)
    requestJson = Column(JSON, default={})
    addedAt = Column(DateTime, default=datetime.datetime.now(datetime.UTC))
    channelId = Column(BigInteger, default=0)