import time
import json
import logging
import threading
from src.store import monitor_store
from src.services import monitor_service

POLL_INTERVAL = 1

logger = logging.getLogger(__name__)


def fire_alert(monitor: dict) -> None:
    alert = {
        "ALERT":          f"Device {monitor['id']} is down!",
        "alert_email":    monitor["alert_email"],
        "time":           time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "last_heartbeat": time.strftime(
                              "%Y-%m-%dT%H:%M:%SZ",
                              time.gmtime(monitor["last_heartbeat"])
                          ),
    }
    print(f"\n{'=' * 50}")
    print(json.dumps(alert, indent=2))
    print(f"{'=' * 50}\n")


def _polling_loop() -> None:
    logger.info(f"[Watchdog] Scheduler started. Polling every {POLL_INTERVAL}s.")

    while True:
        now = time.time()
        all_monitors = monitor_store.get_all_monitors()

        for monitor in all_monitors:
            if (
                monitor["status"] == "active"
                and monitor["expires_at"] is not None
                and monitor["expires_at"] <= now
            ):
                fire_alert(monitor)
                monitor_service.mark_as_down(monitor["id"])

        time.sleep(POLL_INTERVAL)


def start_scheduler() -> None:
    thread = threading.Thread(target=_polling_loop, daemon=True)
    thread.start()
