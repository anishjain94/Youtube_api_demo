from typing import List
import time
from fastapi import Depends, FastAPI, HTTPException, BackgroundTasks
from sqlalchemy.orm import Session
from starlette.requests import Request
from fastapi.testclient import TestClient
from fastapi_pagination import Page, Params, paginate, add_pagination
import asyncio


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
def get_videos(title: str, db: Session = Depends(get_db)):
    return crud.search_videos(title, db)



@app.get("/")
def get_home():
    return {"title" : "Hello world"}


# @app.post("/videos/add")
# async def add_video(start: bool, background_tasks: BackgroundTasks):
#     if start:
#         background_tasks.add_task(add_to_db)

#     return {"status": "processing complete"}





async def add_to_db():  
    db = SessionLocal()
    try:
        crud.add_from_yt(db)
    finally:
        db.close()


if __name__ == "__main__":
    asyncio.run(add_to_db())

add_pagination(app)