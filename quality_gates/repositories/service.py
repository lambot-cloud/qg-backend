from typing import List
from datetime import datetime
from quality_gates.repositories.base import BaseRepository
from quality_gates.repositories.models import Service as ServiceModel
from quality_gates.schemas import Service, ServiceName, InfoSystem, ServiceInfra

from sqlalchemy import select, insert, update, delete, and_
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession


class ServiceRepository(BaseRepository):
    @BaseRepository.handler('Не удалось получить список сервисов')
    async def get_services(self, session: AsyncSession, information_system: str | None = None) -> List[Service]:
        query = select(ServiceModel)
        if information_system:
            query = query.filter(ServiceModel.information_system == information_system)
        result = (await session.execute(query)).scalars().fetchall()

        if result:
            data = [
                {
                    "information_system": r.information_system,
                    "service_name": r.service_name,
                    "monitoring": r.monitoring,
                    "observability": r.observability,
                    "unit_testing_enabled": r.unit_testing_enabled,
                    "unit_testing": r.unit_testing,
                    "description": r.description,
                    "update_date": r.update_date,
                    "git_url": r.git_url,
                    "git_branch": r.git_branch,
                    "ci_pipeline_url": r.ci_pipeline_url,
                    "cm_key": r.cm_key,
                    "qg_status": r.qg_status,
                    "platform": r.platform,
                    "zone": r.zone
                }
                for r in result
            ]
            return [
                Service(
                    **{
                        k: v for k,v in d.items() if v is not None
                    }
                ) for d in data
            ]

        await session.commit()

        return []
    
    @BaseRepository.handler('Не удалось получить список сервисов в информационной системе для инфраструктуры')
    async def get_service_infra_by_is(self, session: AsyncSession, information_system: str) -> List[ServiceInfra]:
        query = select(ServiceModel).where(ServiceModel.information_system == information_system)
        result = (await session.execute(query)).scalars().fetchall()
        
        if result:
            data = [
                {
                    "information_system": r.information_system,
                    "service_name": r.service_name,
                    "monitoring": r.monitoring,
                    "observability": r.observability,
                    "unit_testing_enabled": r.unit_testing_enabled,
                    "unit_testing": r.unit_testing,
                    "description": r.description,
                    "update_date": r.update_date,
                    "git_url": r.git_url,
                    "git_branch": r.git_branch,
                    "ci_pipeline_url": r.ci_pipeline_url,
                    "cm_key": r.cm_key,
                    "qg_status": r.qg_status,
                    "platform": r.platform,
                    "zone": r.zone
                }
                for r in result
            ]
            return [
                ServiceInfra(
                    **{
                        k: v for k,v in d.items() if v is not None
                    }
                ) for d in data
            ]

        await session.commit()

        return []
    @BaseRepository.handler('Не удалось создать или обновить запись о сервисе')
    async def create_or_update(self, session: AsyncSession, service: Service) -> int | None:
        result = await session.execute(
                select(ServiceModel)
                .filter(ServiceModel.information_system == service.information_system)
                .filter(ServiceModel.service_name == service.service_name)
        )
        existing = result.scalars().first()

        service_data = service.dict(exclude_unset=True)

        if existing:
            service_id = existing.id

            await session.execute(
                update(ServiceModel).values(
                    **service_data
                ).where(ServiceModel.id == service_id)
            )
        else:
            result = (
                await session.execute(
                    insert(ServiceModel).values(
                        **service_data
                    ).returning(ServiceModel.id)
                )
            ).fetchone()
            service_id = result[0]

        await session.commit()

        return service_id

    @BaseRepository.handler('Не удалось проверить наличие сервиса')
    async def exists(self, session: AsyncSession, service: ServiceName) -> bool:
        result = await session.execute(
            select(ServiceModel)
            .filter(ServiceModel.information_system == service.information_system)
            .filter(ServiceModel.service_name == service.service_name)
        )
        existing = result.scalars().first()

        await session.commit()

        return bool(existing)

    @BaseRepository.handler('Не удалось удалить сервис')
    async def delete(self, session: AsyncSession, service: ServiceName) -> bool:
        result = await session.execute(
            select(ServiceModel)
            .filter(ServiceModel.information_system == service.information_system)
            .filter(ServiceModel.service_name == service.service_name)
        )
        existing = result.scalars().first()

        result = False
        if existing:
            await session.execute(
                delete(ServiceModel).where(
                    ServiceModel.id == existing.id,
                ).returning(ServiceModel.id)
            )
            result = True

        await session.commit()

        return result
    
    @BaseRepository.handler('Не удалось получить список информационных систем')
    async def get_info_system(self, session: AsyncSession) -> List[InfoSystem]:
        query = select(ServiceModel)
        result = (await session.execute(query)).scalars().fetchall()

        if result:
            data = [
                {
                    "information_system": r.information_system,
                }
                for r in result
            ]
            return [
                InfoSystem(
                    **{
                        k: v for k,v in d.items() if v is not None
                    }
                ) for d in data
            ]

        await session.commit()

        return []
    
    
    @BaseRepository.handler('Не удалось получить CM Key')
    async def get_cm_key(self, session: AsyncSession, service: ServiceName) -> str | None:
        query = select(ServiceModel).where(ServiceModel.information_system == service.information_system, ServiceModel.service_name == service.service_name)
        result = (await session.execute(query)).scalars().first()
        
        if result:
            return result.cm_key
        
        await session.commit()
        
        return None

    @BaseRepository.handler('Не удалось получить список сервисов в информационной системе')
    async def get_service_infra(self, session: AsyncSession, service: ServiceName) -> ServiceInfra:
        query = select(ServiceModel).where(ServiceModel.information_system == service.information_system, ServiceModel.service_name == service.service_name)
        result = (await session.execute(query)).scalars().first()        

        if result:
            return ServiceInfra(
                **{
                    k: v for k,v in result.__dict__.items() if v is not None
                }
            )

        await session.commit()

        return None
        

    
    @BaseRepository.handler('Не удалось записать информационную систему')
    async def set_service_infra(self, session: AsyncSession, service: ServiceInfra) -> bool:
        result = await session.execute(
                select(ServiceModel)
                .filter(ServiceModel.information_system == service.information_system)
                .filter(ServiceModel.service_name == service.service_name)
        )
        existing = result.scalars().first()

        service_data = service.dict(exclude_unset=True)

        if existing:
            service_id = existing.id

            await session.execute(
                update(ServiceModel).values(
                    **service_data
                ).where(ServiceModel.id == service_id)
            )
        else:
            result = (
                await session.execute(
                    insert(ServiceModel).values(
                        **service_data
                    ).returning(ServiceModel.id)
                )
            ).fetchone()
            service_id = result[0]

        await session.commit()

        return service_id