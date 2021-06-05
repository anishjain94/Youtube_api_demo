from sql_app.databases import Base
from typing import List, Optional

from pydantic import BaseModel


class VideoBase(BaseModel):
    title: str


class Video(VideoBase):
    description: str
    published_at: str
    default_thumbnail: str
    medium_thumbnail: str
    high_thumbnail: str


    class Config:
        orm_mode = True
