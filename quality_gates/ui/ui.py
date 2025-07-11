from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from quality_gates.settings import settings

ui_router = APIRouter()

@ui_router.get('/', response_class=HTMLResponse)
async def index(request: Request):
    return RedirectResponse(url=settings.swagger_url)
