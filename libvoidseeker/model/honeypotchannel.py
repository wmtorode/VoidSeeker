from .base import ModelBase
from sqlalchemy import Column, String, Integer, Boolean, Text, BigInteger, ForeignKey, Float, JSON, DateTime


class HoneyPotChannel(ModelBase):
    """

    """
    __tablename__ = "honeyPotChannels"
    id = Column(Integer, index=True, primary_key=True)
    serverId = Column(BigInteger, default=0, index=True)
    messageId = Column(BigInteger, default=0)
    channelId = Column(BigInteger, default=0)
