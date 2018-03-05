from sqlalchemy import Column, Integer, String, Boolean
from .base_model import BaseModel
from .serializable_model import SerializableModel


class Schedule(BaseModel, SerializableModel):

    __tablename__ = 'schedules'

    id = Column(Integer, primary_key=True)
    name = Column(String, default='')
    time = Column(String, nullable=False)
    method = Column(String, nullable=False)
    uri = Column(String, nullable=False)
    parameters = Column(String, default='')
    enable = Column(Boolean, default=True)
    comment = Column(String, default='')
