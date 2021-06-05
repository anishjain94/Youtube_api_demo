from os import name
from sqlalchemy.orm import Session
from sqlalchemy.sql.expression import true, update
import hashlib, binascii, os
from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.sql.functions import mode
from sqlalchemy import or_
import helper
import time
import json



from . import models, schemas



def get_videos(db: Session):
    return db.query(models.Video).all()


def search_videos(title: str, db: Session):
    condition = []
    condition.append(models.Video.title.contains(title))
    condition.append(models.Video.description.contains(title))
    return db.query(models.Video).filter(or_(*condition)).all()


def add_video(video: schemas.Video, db: Session):

    db_item = models.Video(
        title=video.title,
        description=video.description,
        default_thumbnail=video.default_thumbnail,
        published_at=video.published_at,
        medium_thumbnail=video.medium_thumbnail,
        high_thumbnail=video.high_thumbnail,
    )
    print(db_item.__dict__)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item



def add_from_yt(db):
    try:
        request, response = helper.get_videos()

        for obj in response["items"]:
            video_obj = helper.process_response(obj)
            add_video(video_obj, db)

        i = 0
        while i <= 0:
            i = i + 1
            response = helper.next_response(request, response)
            time.sleep(10)

            for obj in response["items"]:
                video_obj = helper.process_response(obj)
                temp = add_video(video_obj, db)

        return {"status": "processing complete"}
        
    except Exception as e:
        print(e)