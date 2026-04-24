from pydantic import BaseModel, ConfigDict, Field
from typing import List, Optional


class PartCreate(BaseModel):
    name: str
    price: Optional[float] = None
    quantity: int = 1
    parent_id: Optional[int] = None


class PartResponse(BaseModel):
    id: int
    name: str
    price: float
    quantity: int
    children: List["PartResponse"] = Field(default_factory=list)

    model_config = ConfigDict(from_attributes=True)

class PartUpdate(BaseModel):
    name: Optional[str] = None
    price: Optional[float] = None
    quantity: Optional[int] = None
    parent_id: Optional[int] = None

    
PartResponse.model_rebuild()