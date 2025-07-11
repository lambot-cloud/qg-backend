from typing import List
from fastapi import APIRouter, HTTPException, Depends

# from api.models.response import server_error, success
from quality_gates.schemas import ServiceInfra, ServiceName
from quality_gates.depends import has_access, get_services_service

infra_router = APIRouter(prefix="/infrastructure")


@infra_router.get('/services/{information_system}', response_model=List[ServiceInfra])
async def get_services(
        information_system,
        service=Depends(get_services_service),
        _=Depends(has_access)
):
    """
    get list of all services in information_system

    """
    return await service.get_service_infra_by_is(information_system=information_system)

@infra_router.post('/service/get', response_model=ServiceInfra)
async def get_services(
        record: ServiceName,
        service=Depends(get_services_service),
        _=Depends(has_access)
):
    """
    get list of all services in information_system

    """
    return await service.get_service_infra(service=record)

@infra_router.post('/service/set')
async def set_service_infra(
        record: ServiceInfra,
        service=Depends(get_services_service),
        _=Depends(has_access)
):
    """
    set service infrastructure
    """
    result = await service.set_service_infra(service=record)
    if result:
        raise HTTPException(status_code=200, detail="Service infrastructure updated")
    elif not result:
        raise HTTPException(status_code=404, detail="Service not found")
    else:
        raise HTTPException(status_code=404, detail="Что-то случилось")