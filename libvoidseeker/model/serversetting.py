from .base import ModelBase
from sqlalchemy import Column, String, Integer, Boolean, Text, BigInteger, ForeignKey, Float, JSON, DateTime, Unicode, UnicodeText
import datetime


class ServerSetting(ModelBase):
    """

    """
    __tablename__ = "serverSettings"
    id = Column(Integer, index=True, primary_key=True)
    serverId = Column(BigInteger, default=0, index=True)
    honeyPotEnabled = Column(Boolean, default=False)
    honeyPotText = Column(UnicodeText, default="")
    heuristicsEnabled = Column(Boolean, default=False)
    banOnPingAll = Column(Boolean, default=False)
    createdAt = Column(DateTime, default=datetime.datetime.now(datetime.UTC))
    updatedAt = Column(DateTime)

