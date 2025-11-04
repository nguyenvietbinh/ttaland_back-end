from pydantic import BaseModel, Field, validator
from typing import Optional, List, Literal
from datetime import datetime

class Media(BaseModel):
    images: List[str] = Field(default_factory=list)
    youtube_url: Optional[str] = None
    tiktok_url: Optional[str] = None

class BaseProduct(BaseModel):
    id: str = Field(..., min_length=1)
    title: str = Field(..., min_length=1)
    location: str = Field(..., min_length=1)
    latitude: str
    longitude: str
    detail_location: str
    price: float = Field(..., gt=0)
    area: float = Field(..., gt=0)
    description: str
    created_at: str
    policy: Optional[str] = None
    entranceWay: Optional[int] = Field(None, ge=0)
    media: Media

    @validator('created_at')
    def validate_date_format(cls, v):
        try:
            datetime.fromisoformat(v.replace('Z', '+00:00'))
            return v
        except ValueError:
            raise ValueError('Invalid date format, expected ISO format')

class Townhouse(BaseProduct):
    type: Literal['townhouse']
    bedroom: int = Field(..., ge=0)
    bathroom: int = Field(..., ge=0)
    numberOfFloors: Optional[str] = None
    interior: Optional[str] = None

class Villa(BaseProduct):
    type: Literal['villa']
    bedroom: int = Field(..., ge=0)
    bathroom: int = Field(..., ge=0)
    numberOfFloors: Optional[str] = None
    interior: Optional[str] = None

class Land(BaseProduct):
    type: Literal['land']
    # Land không có bedroom, bathroom, numberOfFloors, interior

class Apartment(BaseProduct):
    type: Literal['apartment']
    bedroom: int = Field(..., ge=0)
    bathroom: int = Field(..., ge=0)
    numberOfFloors: Optional[str] = None
    interior: Optional[str] = None

# Product container
class ProductContainer(BaseModel):
    product: Townhouse | Villa | Land | Apartment

    class Config:
        # Cho phép tự động detect type dựa trên field 'type'
        smart_union = True