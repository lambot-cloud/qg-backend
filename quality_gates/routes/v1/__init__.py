from fastapi import APIRouter
from .monitoring import mon_router
from .release import release_router
from .infra import infra_router
from .trusted import trusted_router

v1_api = APIRouter(prefix="/api/v1")
v1_api.include_router(mon_router, tags=["monitoring"])
v1_api.include_router(release_router, tags=["release"])
v1_api.include_router(infra_router, tags=["infrastructure"])
v1_api.include_router(trusted_router, tags=["trusted"])



__all__ = (v1_api,)
