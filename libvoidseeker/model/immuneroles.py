from .base import ModelBase
from sqlalchemy import Column, String, Integer, Boolean, Text, BigInteger, ForeignKey, Float, JSON, DateTime, Unicode
import datetime


class ImmuneRole(ModelBase):
    """

    """
    __tablename__ = "immuneRoles"
    id = Column(Integer, index=True, primary_key=True)
    serverId = Column(BigInteger, default=0, index=True)
    roleId = Column(BigInteger, default=0)
    addedByUserId = Column(BigInteger, default=0)
    createdAt = Column(DateTime, default=datetime.datetime.now(datetime.UTC))