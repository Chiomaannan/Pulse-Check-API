import time
from contextlib import asynccontextmanager
from fastapi import FastAPI
from src.routes.monitors import router as monitors_router
from src.scheduler.watchdog_scheduler import start_scheduler


@asynccontextmanager
async def lifespan(app: FastAPI):
    start_scheduler()
    yield


app = FastAPI(
    title="Watchdog Sentinel API",
    description=(
        "A Dead Man's Switch API for monitoring remote devices. "
        "Devices register a monitor with a timeout. If they stop "
        "sending heartbeats, an alert is triggered automatically."
    ),
    version="1.0.0",
    lifespan=lifespan,
)


@app.get("/health", tags=["Health"])
def health_check():
    return {
        "status": "ok",
        "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
    }


app.include_router(monitors_router)
