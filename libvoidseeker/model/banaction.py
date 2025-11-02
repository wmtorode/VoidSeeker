from .base import ModelBase
from sqlalchemy import Column, String, Integer, Boolean, Text, BigInteger, ForeignKey, Float, JSON, DateTime, Unicode
import datetime


class BanAction(ModelBase):
    """

    """
    __tablename__ = "banActions"
    id = Column(Integer, index=True, primary_key=True)
    serverId = Column(BigInteger, default=0, index=True)
    userId = Column(BigInteger, default=0)
    bannedAt = Column(DateTime, default=datetime.datetime.now(datetime.UTC))
    userName = Column(Unicode(length=64), default="")
    createdAt = Column(DateTime)
    joinedAt = Column(DateTime)
    detectionMethod = Column(String(length=64), default="")
    banId = Column(Integer, default=0)

    @property
    def pStat(self):
        return f'{self.banId:<8} {self.userName:<34} {self.bannedAt.isoformat(sep=" ", timespec="minutes"):>18} {self.userId}\n'

