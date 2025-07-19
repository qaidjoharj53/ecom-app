from pydantic import BaseModel
from typing import Optional, List

class PaginationInfo(BaseModel):
    next: Optional[str]
    limit: int
    previous: Optional[str]

class BaseResponse(BaseModel):
    id: str

class BasePaginatedResponse(BaseModel):
    page: PaginationInfo