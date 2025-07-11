from typing import List
from fastapi import APIRouter, HTTPException, Depends

# from api.models.response import server_error, success
from quality_gates.schemas import Service, ServiceName
from quality_gates.depends import get_services_service, has_access

mon_router = APIRouter(prefix="/monitoring")


@mon_router.post("/update")
async def update_service(
        record: Service,
        service=Depends(get_services_service),
        _=Depends(has_access)
) -> int:
    """
    Create or update records in database of service monitoring
    """
    return await service.create_or_update(service=record)


@mon_router.get('/services/{information_system}', response_model=List[Service])
async def get_services(
        information_system,
        service=Depends(get_services_service),
        _=Depends(has_access)
):
    """
    get list of all services in information_system

    """
    return await service.get_services_by_is(information_system=information_system)


@mon_router.get('/services', response_model=List[Service])
async def get_all_services(
        service=Depends(get_services_service),
        _=Depends(has_access)
):
    """
    get list of all services

    """
    return await service.get_all_services()


@mon_router.delete('/services')
async def delete_service_record(
        record: ServiceName,
        service=Depends(get_services_service),
        _=Depends(has_access)
):
    """
    delete service record
    """
    result = await service.delete_service(record)
    if not result:
        raise HTTPException(status_code=404, detail="Service not found")
    
@mon_router.get('/info_system')
async def get_info_system(
        service=Depends(get_services_service),
        _=Depends(has_access)
):
    """
    get list of all information systems

    """
    return await service.get_info_system()
