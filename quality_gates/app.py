from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from quality_gates.routes.v1 import v1_api
from quality_gates.ui import v1_ui
from quality_gates.repositories.base import engine
from quality_gates.settings import settings


from prometheus_fastapi_instrumentator import Instrumentator



docs_url=None if settings.swagger == False else "/api/docs"
redoc_url=None if settings.swagger == False else "/api/redoc"
openapi_url=None if settings.swagger == False else "/openapi.json"

app = FastAPI(docs_url=docs_url, redoc_url=redoc_url, openapi_url=openapi_url, title="Quality Gates")


app.include_router(v1_api)
app.include_router(v1_ui)

Instrumentator().instrument(app).expose(app, tags=["metrics"])

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health", tags=["HealthCheck"])
def health():
    return "Healthy"


@app.on_event("startup")
async def startup():
    pass

@app.on_event("shutdown")
async def shutdown():
    await engine.dispose()
