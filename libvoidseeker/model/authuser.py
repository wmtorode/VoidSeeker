from .base import ModelBase
from sqlalchemy import Column, String, Integer, Boolean, Text, BigInteger, ForeignKey, Float, JSON, DateTime, Unicode
import datetime


class AuthUser(ModelBase):
    """

    """
    __tablename__ = "authUsers"
    id = Column(Integer, index=True, primary_key=True)
    serverId = Column(BigInteger, default=0, index=True)
    userId = Column(BigInteger, default=0)
    userName = Column(Unicode(length=64), default="")
    addedAt = Column(DateTime, default=datetime.datetime.now(datetime.UTC))
    updatedAt = Column(DateTime, default=datetime.datetime.now(datetime.UTC))
    role = Column(String(length=64), default="")
