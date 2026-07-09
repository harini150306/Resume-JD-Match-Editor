from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from app.routers import parse, auth
from app.database import Base, engine

# Create DB tables on startup if they don't exist yet
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Resume-JD Matcher", version="0.1.0")

# Allow local frontend to call the API during development
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router, prefix="/api/auth", tags=["auth"])
app.include_router(parse.router, prefix="/api", tags=["parse"])


@app.get("/health")
def health_check():
    return {"status": "ok"}


# Serve the frontend. Must be mounted AFTER the API routes above,
# since this mount ("/") would otherwise catch every request first.
app.mount("/", StaticFiles(directory="frontend", html=True), name="frontend")