from typing import List
import time
from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session
from starlette.requests import Request
from fastapi.testclient import TestClient
from fastapi_pagination import Page, Params, paginate, add_pagination


from sql_app import crud, models, schemas
from sql_app.databases import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()



@app.get("/videos/all/", response_model=Page[schemas.Video])
def get_videos(db: Session = Depends(get_db)):
    videos = crud.get_videos(db)
    return paginate(videos)



@app.get("/videos/search/", response_model=List[schemas.Video])
def get_videos(title : str, db: Session = Depends(get_db)):
    return crud.search_videos(title, db)



@app.post("/videos/add", response_model = schemas.Video)
def add_video(start: bool, db: Session = Depends(get_db)):
    if start:
        return crud.add_from_yt(db)
    

add_pagination(app)
