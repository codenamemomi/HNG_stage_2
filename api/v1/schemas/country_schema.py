from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class CountryBase(BaseModel):
    name: str = Field(..., description="Country name")
    capital: Optional[str] = None
    region: Optional[str] = None
    population: int = Field(..., ge=0)
    currency_code: Optional[str] = None
    exchange_rate: Optional[float] = None
    estimated_gdp: Optional[float] = None
    flag_url: Optional[str] = None

class CountryCreate(CountryBase):
    pass

class CountryResponse(CountryBase):
    id: int
    last_refreshed_at: datetime

    class Config:
        orm_mode = True
