from __future__ import annotations

from fastapi import APIRouter, Header, HTTPException
from pydantic import BaseModel

from api.support import require_admin
from services.auth_service import auth_service


class ExternalKeyRequest(BaseModel):
    key: str


def create_router() -> APIRouter:
    router = APIRouter()

    # Custom integration endpoints for mirroring keys from the caller's service.
    @router.post("/api/external/auth/keys/sync")
    async def sync_external_key(
        body: ExternalKeyRequest,
        authorization: str | None = Header(default=None),
    ):
        require_admin(authorization)
        try:
            auth_service.sync_user_key(body.key)
        except ValueError as exc:
            raise HTTPException(status_code=400, detail={"error": "sync key failed"}) from exc
        return {"ok": True}

    @router.delete("/api/external/auth/keys")
    async def delete_external_key(
        body: ExternalKeyRequest,
        authorization: str | None = Header(default=None),
    ):
        require_admin(authorization)
        try:
            auth_service.delete_user_key_by_raw_key(body.key)
        except ValueError as exc:
            raise HTTPException(status_code=400, detail={"error": "sync key failed"}) from exc
        return {"ok": True}

    return router
