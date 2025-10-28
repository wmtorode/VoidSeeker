from .base import ModelBase
from sqlalchemy import Column, String, Integer, Boolean, Text, BigInteger, ForeignKey, Float, JSON, DateTime, Unicode
import datetime


class BanTerm(ModelBase):
    """

    """
    __tablename__ = "banTerms"
    id = Column(Integer, index=True, primary_key=True)
    serverId = Column(BigInteger, default=0, index=True)
    term = Column(Unicode(length=256), default="")
    termType = Column(String(length=256), default="")
    addedByUserId = Column(BigInteger, default=0)
    createdAt = Column(DateTime, default=datetime.datetime.now(datetime.UTC))
