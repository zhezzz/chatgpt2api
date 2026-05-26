from __future__ import annotations

from fastapi import APIRouter, Header, HTTPException
from pydantic import BaseModel

from api.support import require_admin
from services.auth_service import auth_service


class ExternalKeySyncRequest(BaseModel):
    email: str
    key: str
    enabled: bool = True


def create_router() -> APIRouter:
    router = APIRouter()

    # Custom integration endpoint for syncing user keys from the caller's service.
    @router.post("/api/external/auth/keys/sync")
    async def sync_external_key(
        body: ExternalKeySyncRequest,
        authorization: str | None = Header(default=None),
    ):
        require_admin(authorization)
        try:
            auth_service.sync_user_key(email=body.email, key=body.key, enabled=body.enabled)
        except ValueError as exc:
            raise HTTPException(status_code=400, detail={"error": "sync key failed"}) from exc
        return {"ok": True}

    return router
