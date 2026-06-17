from typing import Optional

_monitors: dict[str, dict] = {}


def set_monitor(monitor: dict) -> None:
    _monitors[monitor["id"]] = monitor


def get_monitor(monitor_id: str) -> Optional[dict]:
    return _monitors.get(monitor_id)


def get_all_monitors() -> list[dict]:
    return list(_monitors.values())


def monitor_exists(monitor_id: str) -> bool:
    return monitor_id in _monitors


def delete_monitor(monitor_id: str) -> None:
    _monitors.pop(monitor_id, None)
