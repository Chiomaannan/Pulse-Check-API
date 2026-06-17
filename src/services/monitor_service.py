import time
from src.store import monitor_store


def create_monitor(monitor_id: str, timeout: int, alert_email: str) -> dict:
    if monitor_store.monitor_exists(monitor_id):
        return {"success": False, "reason": "ALREADY_EXISTS"}

    now = time.time()
    monitor = {
        "id":             monitor_id,
        "timeout":        timeout,
        "alert_email":    alert_email,
        "status":         "active",
        "expires_at":     now + timeout,
        "last_heartbeat": now,
        "created_at":     now,
    }

    monitor_store.set_monitor(monitor)
    return {"success": True, "monitor": monitor}


def heartbeat(monitor_id: str) -> dict:
    monitor = monitor_store.get_monitor(monitor_id)
    if not monitor:
        return {"success": False, "reason": "NOT_FOUND"}

    now = time.time()
    monitor["status"]         = "active"
    monitor["expires_at"]     = now + monitor["timeout"]
    monitor["last_heartbeat"] = now

    monitor_store.set_monitor(monitor)
    return {"success": True, "monitor": monitor}


def pause_monitor(monitor_id: str) -> dict:
    monitor = monitor_store.get_monitor(monitor_id)
    if not monitor:
        return {"success": False, "reason": "NOT_FOUND"}

    if monitor["status"] == "paused":
        return {"success": False, "reason": "ALREADY_PAUSED"}

    monitor["status"]     = "paused"
    monitor["expires_at"] = None

    monitor_store.set_monitor(monitor)
    return {"success": True, "monitor": monitor}


def get_monitor(monitor_id: str) -> dict:
    monitor = monitor_store.get_monitor(monitor_id)
    if not monitor:
        return {"success": False, "reason": "NOT_FOUND"}
    return {"success": True, "monitor": monitor}


def get_all_monitors() -> dict:
    return {"success": True, "monitors": monitor_store.get_all_monitors()}


def mark_as_down(monitor_id: str) -> None:
    monitor = monitor_store.get_monitor(monitor_id)
    if not monitor:
        return

    monitor["status"]     = "down"
    monitor["expires_at"] = None
    monitor_store.set_monitor(monitor)
