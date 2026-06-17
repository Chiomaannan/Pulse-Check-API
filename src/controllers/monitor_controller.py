import time
from fastapi import HTTPException
from pydantic import BaseModel, field_validator
from src.services import monitor_service


class RegisterRequest(BaseModel):
    id: str
    timeout: int
    alert_email: str

    @field_validator("timeout")
    @classmethod
    def timeout_must_be_positive(cls, v):
        if v <= 0:
            raise ValueError("timeout must be a positive integer (seconds)")
        return v

    @field_validator("id")
    @classmethod
    def id_must_not_be_empty(cls, v):
        if not v.strip():
            raise ValueError("id must not be empty")
        return v


def register_monitor(body: RegisterRequest):
    result = monitor_service.create_monitor(
        monitor_id=body.id,
        timeout=body.timeout,
        alert_email=body.alert_email,
    )

    if not result["success"] and result["reason"] == "ALREADY_EXISTS":
        raise HTTPException(
            status_code=409,
            detail=f"Monitor '{body.id}' already exists"
        )

    return {
        "message": f"Monitor '{body.id}' registered successfully.",
        "monitor": result["monitor"]
    }


def heartbeat(monitor_id: str):
    result = monitor_service.heartbeat(monitor_id)

    if not result["success"] and result["reason"] == "NOT_FOUND":
        raise HTTPException(
            status_code=404,
            detail=f"Monitor '{monitor_id}' not found"
        )

    monitor = result["monitor"]
    return {
        "message": f"Heartbeat received for '{monitor_id}'. Timer reset.",
        "expires_at": time.strftime(
            "%Y-%m-%dT%H:%M:%SZ",
            time.gmtime(monitor["expires_at"])
        )
    }


def pause_monitor(monitor_id: str):
    result = monitor_service.pause_monitor(monitor_id)

    if not result["success"]:
        if result["reason"] == "NOT_FOUND":
            raise HTTPException(
                status_code=404,
                detail=f"Monitor '{monitor_id}' not found"
            )
        if result["reason"] == "ALREADY_PAUSED":
            raise HTTPException(
                status_code=409,
                detail=f"Monitor '{monitor_id}' is already paused"
            )

    return {
        "message": f"Monitor '{monitor_id}' paused. No alerts will fire.",
        "monitor": result["monitor"]
    }


def get_monitor(monitor_id: str):
    result = monitor_service.get_monitor(monitor_id)

    if not result["success"]:
        raise HTTPException(
            status_code=404,
            detail=f"Monitor '{monitor_id}' not found"
        )

    return {"monitor": result["monitor"]}


def get_all_monitors():
    result = monitor_service.get_all_monitors()
    return result
