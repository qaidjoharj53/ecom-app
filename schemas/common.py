from pydantic import BaseModel
from typing import Optional, List

class PaginationInfo(BaseModel):
    next: Optional[str]
    limit: int
    previous: Optional[int]

class BasePaginatedResponse(BaseModel):
    page: PaginationInfo