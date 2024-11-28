from fastapi import FastAPI
from app.routes.users import user_router  # assuming the router name from routes/users.py
from app.routes.statistics import statistics_router
from app.database.connection import conn
import uvicorn
import os
from dotenv import load_dotenv

async def lifespan(app: FastAPI):
    # on start up
    conn()
    yield
    # on exit

app = FastAPI(root_path='/api', lifespan=lifespan)

@app.get("/")
def world():
    return {"hello world"}

app.include_router(user_router)
app.include_router(statistics_router)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
