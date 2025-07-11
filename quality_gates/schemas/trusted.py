from typing import List
from pydantic import BaseModel, Field


class Trusted(BaseModel):
    image_name: str
    image_url: str
    image_status: str
    
class TrustedByName(BaseModel):
    image_name: str
    
class TrustedByUrl(BaseModel):
    image_url: str