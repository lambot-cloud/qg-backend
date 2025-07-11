from typing import Annotated
from fastapi import Depends, HTTPException
from fastapi.security import APIKeyQuery

from quality_gates.repositories import ServiceRepository, TrustedRepository
from quality_gates.services import ServicesService
from quality_gates.schemas import Service

from quality_gates.settings import settings


# oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
query_scheme = APIKeyQuery(name="token")

repository = ServiceRepository()
service = ServicesService(repository)
trusted_repository = TrustedRepository()

def get_trusted_repository() -> TrustedRepository:
    return trusted_repository


def get_services_service() -> ServicesService:
    return service


async def has_access(token: Annotated[str, Depends(query_scheme)]) -> bool:
    if token != settings.api_token.get_secret_value():
        raise HTTPException(status_code=401, detail='Unauthorized')

    return True
