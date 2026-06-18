from fastapi import APIRouter
from src.controllers.monitor_controller import (
    RegisterRequest,
    register_monitor,
    heartbeat,
    pause_monitor,
    get_monitor,
    get_all_monitors,
)

router = APIRouter(prefix="/monitors", tags=["Monitors"])

router.post("", status_code=201)(register_monitor)
router.post("/{monitor_id}/heartbeat")(heartbeat)
router.post("/{monitor_id}/pause")(pause_monitor)
router.get("/{monitor_id}")(get_monitor)
router.get("")(get_all_monitors)
