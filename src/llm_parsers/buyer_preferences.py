from pydantic import BaseModel, Field
from typing import Optional, List

# Defining a pydantic output parser for our query cleaning LLM
class BuyerPreferences(BaseModel):
    bedrooms: Optional[int] = Field(None, description="Number of bedrooms")
    bathrooms: Optional[int] = Field(None, description="Number of bathrooms")
    house_size: Optional[str] = Field(None, description="Desired house size (e.g. '2000 sqft')")
    amenities: Optional[List[str]] = Field(None, description="Desired amenities (e.g. backyard, solar panels)")
    transportation: Optional[List[str]] = Field(None, description="Transportation preferences (e.g. bike paths, public transit)")
    neighborhood_traits: Optional[List[str]] = Field(None, description="Neighborhood qualities (e.g. quiet, walkable)")
    price_range: Optional[str] = Field(None, description="Approximate price range or budget")
    lifestyle: Optional[str] = Field(None, description="Lifestyle fit, e.g. remote work, family-friendly")
    query: str = Field(..., description="One concise summary sentence combining the above preferences, the summary should be optimize for similarity search in avector database")