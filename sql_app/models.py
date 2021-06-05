from typing import List
from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from sqlalchemy.sql.expression import true
from sqlalchemy.sql.sqltypes import Float

from .databases import Base


class Video(Base):
    __tablename__ = "video"
    id = Column(Integer, autoincrement=True, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(String)
    published_at = Column(String)
    
    default_thumbnail = Column(String)
    medium_thumbnail = Column(String)
    high_thumbnail = Column(String)
