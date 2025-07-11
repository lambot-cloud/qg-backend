from typing import List
from quality_gates.repositories import ServiceRepository
from quality_gates.schemas import Service, ServiceName, InfoSystem, ServiceInfra


class ServicesService:
    def __init__(self, repository: ServiceRepository):
        self.repository = repository

    async def get_services_by_is(self, information_system: str) -> List[Service]:
        return (
            await self.repository.get_services(information_system=information_system)
        )
        
    async def get_service_infra_by_is(self, information_system: str) -> List[Service]:
        return (
            await self.repository.get_service_infra_by_is(information_system=information_system)
        )

    async def get_all_services(self) -> List[Service]:
        return (
            await self.repository.get_services()
        )

    async def create_or_update(self, service: Service) -> int | None:
        return (
            await self.repository.create_or_update(service=service)
        )

    async def delete_service(self, service: ServiceName) -> bool:
        exists = await self.repository.exists(service)

        result = False
        if exists:
            result = await self.repository.delete(service)

        return result
    
    async def set_cm_key(self, service: ServiceName) -> bool:
        exists = await self.repository.exists(service)

        result = False
        if exists:
            result = await self.repository.create_or_update(service)

        return result
    
    async def get_info_system(self: str) -> List[InfoSystem]:
        return (
            await self.repository.get_info_system()
        )
        
    async def get_cm_key(self, service: ServiceName) -> str | None:
        return (
            await self.repository.get_cm_key(service)
        )
        
    async def get_service_infra(self, service: ServiceName) -> ServiceInfra:
        return (
            await self.repository.get_service_infra(service)
        )
        
    async def set_service_infra(self, service: ServiceInfra) -> bool:
        return (
            await self.repository.set_service_infra(service)
        )
