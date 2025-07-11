from typing import List
from datetime import datetime
from quality_gates.repositories.base import BaseRepository
from quality_gates.repositories.models import Trusted as TrustedModel
from quality_gates.schemas import Trusted, TrustedByName, TrustedByUrl

from sqlalchemy import select, insert, update, delete, and_
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession


# get all trusted images
class TrustedRepository(BaseRepository):
    @BaseRepository.handler('Не удалось получить список доверенных образов')
    async def get_trusted(self, session: AsyncSession) -> List[Trusted]:
        query = select(TrustedModel)
        result = (await session.execute(query)).scalars().fetchall()

        if result:
            data = [
                {
                    "image_name": r.image_name,
                    "image_url": r.image_url,
                    "image_status": r.image_status,
                }
                for r in result
            ]            
            return [
                Trusted(
                    **{
                        k: v for k,v in d.items() if v is not None
                    }
                ) for d in data
            ]

        await session.commit()

        return []
    
    # get all images by image_name, return list of Trusted
    @BaseRepository.handler('Не удалось получить список доверенных образов')
    async def get_trusted_by_name(self, session: AsyncSession, image_name: str) -> List[TrustedByUrl]:
        query = select(TrustedModel).where(TrustedModel.image_name == image_name)
        result = (await session.execute(query)).scalars().fetchall()
        if result:
            data = [
                {
                    "image_url": r.image_url
                }
                for r in result
            ]            
            return [
                TrustedByUrl(
                    **{
                        k: v for k,v in d.items() if v is not None
                    }
                ) for d in data
            ]
            
            
        await session.commit()
        return []

    
    #get image by image_url
    @BaseRepository.handler('Не удалось получить доверенный образ')
    async def get_trusted_by_url(self, session: AsyncSession, image_url: str) -> TrustedByUrl:
        query = select(TrustedModel).where(TrustedModel.image_url == image_url)
        result = (await session.execute(query)).scalars().first()

        if result:
            return TrustedByUrl(
                **{
                    k: v for k,v in result.__dict__.items() if v is not None
                }
            )
        
        await session.commit()
        
        return None
    
        
    @BaseRepository.handler('Не удалось создать или обновить запись о доверенном образе')
    async def create_or_update(self, session: AsyncSession, trusted: Trusted) -> int | None:
        result = await session.execute(
                select(TrustedModel)
                .filter(TrustedModel.image_url == trusted.image_url)
        )
        existing = result.scalars().first()

        trusted_data = trusted.dict(exclude_unset=True)

        if existing:
            trusted_id = existing.id

            await session.execute(
                update(TrustedModel).values(
                    **trusted_data
                ).where(TrustedModel.id == trusted_id)
            )
        else:
            result = (
                await session.execute(
                    insert(TrustedModel).values(
                        **trusted_data
                    ).returning(TrustedModel.id)
                )
            ).fetchone()
            trusted_id = result[0]

        await session.commit()

        return trusted_id

    @BaseRepository.handler('Не удалось удалить доверенный образ')
    async def delete(self, session: AsyncSession, image_url: str) -> bool:
        result = await session.execute(
            select(TrustedModel)
            .filter(TrustedModel.image_url == image_url)
        )
        existing = result.scalars().first()

        result = False
        if existing:
            await session.execute(
                delete(TrustedModel).where(
                    TrustedModel.id == existing.id,
                ).returning(TrustedModel.id)
            )
            result = True

        await session.commit()

        return result
    