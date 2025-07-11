from typing import List
from pydantic import BaseModel, Field


class ServiceName(BaseModel):
    information_system: str
    service_name: str
    
class ServiceCM(BaseModel):
    information_system: str
    service_name: str
    cm_key: str
    
class InfoSystem(BaseModel):
    information_system: str
    
class Comment(BaseModel):
    service_name: str
    pipeline_url: str
    executor: str
    version: str
    
class Service(ServiceName):
    monitoring: bool | None = Field(default=None)
    observability: bool | None = Field(default=None)
    unit_testing_enabled: bool | None = Field(default=None)
    unit_testing: str | None = Field(default_factory=str)
    update_date: str | None = Field(default=None)
    description: str | None = Field(default=None)
    git_url: str | None = Field(default=None)
    git_branch: str | None = Field(default=None)
    ci_pipeline_url: str | None = Field(default=None)
    cm_key: str | None = Field(default=None)
    qg_status: str | None = Field(default=None)

class ServiceInfra(ServiceName):
    platform: str | None = Field(default=None)
    zone: str | None = Field(default=None)
