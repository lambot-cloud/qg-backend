from typing import List
from fastapi import APIRouter, HTTPException, Depends

# from api.models.response import server_error, success
from quality_gates.schemas import Trusted
from quality_gates.depends import has_access, trusted_repository


trusted_router = APIRouter(prefix="/trusted")

@trusted_router.post("/update/image", operation_id="update_trusted_image")
async def update_trusted(
        record: Trusted,
        _=Depends(has_access)
) -> int:
    """
    Create or update records in database of trusted images
    """
    return await trusted_repository.create_or_update(trusted=record)

@trusted_router.get('/images/all', operation_id="get_all_trusted_images")
async def get_trusted(
        _=Depends(has_access)
):
    """
    get list of all trusted images
    """
    return await trusted_repository.get_trusted()

@trusted_router.get('/images/{image_name}', operation_id="get_trusted_image_by_name")
async def get_trusted_by_name(
        image_name,
        _=Depends(has_access)
):
    """
    get list of all trusted images
    """
    return await trusted_repository.get_trusted_by_name(image_name)


@trusted_router.post('/image/get', operation_id="get_trusted_image_by_url")
async def get_trusted_by_url(
        image_url,
        _=Depends(has_access)
):
    """
    get trusted images
    """
    return await trusted_repository.get_trusted_by_url(image_url)


@trusted_router.delete('/delete', operation_id="delete_trusted_image")
async def delete_trusted(
        image_url,
        _=Depends(has_access)
):
    """
    delete trusted image
    """
    result = await trusted_repository.delete(image_url)
    if not result:
        raise HTTPException(status_code=404, detail="Trusted image not found")
    else:
        raise HTTPException(status_code=200, detail="Trusted image deleted")
    
    