from typing import List
from quality_gates.repositories import TrustedRepository
from quality_gates.schemas import Trusted


class TrustedImages:
    def __init__(self, repository: TrustedRepository):
        self.repository = repository

    async def get_trusted(self) -> List[Trusted]:
        return (
            await self.repository.get_trusted()
        )

    async def get_trusted_by_name(self, image_name: str) -> Trusted:
        return (
            await self.repository.get_trusted_by_name(image_name)
        )

    async def create_or_update(self, trusted: Trusted) -> int | None:
        return (
            await self.repository.create_or_update(trusted)
        )

    async def delete(self, image_name: str) -> bool:
        exists = await self.repository.exists(image_name)

        result = False
        if exists:
            result = await self.repository.delete(image_name)

        return result
