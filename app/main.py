from fastapi import FastAPI
from .db.database import engine
from .models import transcription, folder, log

# Create the database tables
transcription.Base.metadata.create_all(bind=engine)
folder.Base.metadata.create_all(bind=engine)
log.Base.metadata.create_all(bind=engine)

from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from .api import folders, jobs, logs, settings

app = FastAPI(
    title="Automated Audio Transcription Monitor",
    description="A service to monitor folders for audio files and transcribe them automatically.",
    version="0.1.0",
)

app.mount("/static", StaticFiles(directory="app/static"), name="static")

from .core.worker import start_worker

app.include_router(folders.router, prefix="/api")
app.include_router(jobs.router, prefix="/api")
app.include_router(logs.router, prefix="/api")
app.include_router(settings.router, prefix="/api")

@app.on_event("startup")
async def startup_event():
    start_worker()

@app.get("/")
async def read_index():
    return FileResponse('app/static/index.html')