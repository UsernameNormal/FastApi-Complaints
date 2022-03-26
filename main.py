import databases
from fastapi import FastAPI
from resources.routes import api_router
from db.config import database
import uvicorn

app = FastAPI()
app.include_router(api_router)


@app.on_event('startup')
async def startup():
    await database.connect()


@app.on_event('shutdown')
async def shutdown():
    await database.disconnect()

if __name__ == "__main__":
    
    uvicorn.run(app)