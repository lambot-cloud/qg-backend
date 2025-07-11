from typing import List
from fastapi import APIRouter, HTTPException, Depends
from fastapi.responses import JSONResponse

# from api.models.response import server_error, success
from quality_gates.schemas import Comment, ServiceCM, ServiceName
from quality_gates.depends import has_access, get_services_service
from quality_gates.core.release_check import jira
from quality_gates.core.templates import jira_template
from quality_gates.utils.logger import logger


release_router = APIRouter(prefix="/release")


@release_router.get('/check/{issue_key}')
async def get_release_check(
        issue_key
	):
    try:
        result = jira.jiraFilter(issue_key=issue_key)
    except Exception as e:
        raise HTTPException(status_code=404, detail=f"Can`t get issue {issue_key}")
    if result:
        raise HTTPException(status_code=200, detail=result)
    else:
        raise HTTPException(status_code=400, detail=result)
    
    
@release_router.post('/comment/{issue_key}')
async def comment_issue(
        issue_key,
        info: Comment,
        _=Depends(has_access)
        ):
        result = jira.comment_issue(issue_key=issue_key, comment=jira_template(info))
        logger.info(f"Comment added to issue {issue_key}")
        if result:
            raise HTTPException(status_code=200, detail="Comment added")
        else:
            raise HTTPException(status_code=400, detail="Can`t add comment")
        
        
@release_router.post("/cm/set")
async def set_cm_key(
        record: ServiceCM,
        service=Depends(get_services_service),
        _=Depends(has_access)
):
    cm_check = jira.checkIssue(record.cm_key)
    if cm_check == True:
        result = await service.set_cm_key(service=record)
        if result:
            raise HTTPException(status_code=200, detail="CM Key updated")
        elif not result:
            raise HTTPException(status_code=404, detail="Service not found")
        else:
            raise HTTPException(status_code=404, detail="Что-то случилось")
    else:
        raise HTTPException(status_code=404, detail="Проверьте ключ CM")
    
    
@release_router.post("/cm/get")
async def get_cm_key(
        record:ServiceName,
        service=Depends(get_services_service),
):
    result = await service.get_cm_key(service=record)
    if result:
        raise HTTPException(status_code=200, detail=result)
    elif not result:
        raise HTTPException(status_code=404, detail="Service not found")
    else:
        raise HTTPException(status_code=404, detail="Что-то случилось")
    







