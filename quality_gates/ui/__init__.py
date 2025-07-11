from fastapi import APIRouter
from .ui import ui_router

v1_ui = APIRouter()
v1_ui.include_router(ui_router, tags=["ui"])

__all__ = (v1_ui,)
