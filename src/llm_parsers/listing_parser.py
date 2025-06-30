from pydantic import BaseModel, Field


# defining a Pydantic outputparser to format the llm output
class Listing(BaseModel):
    neighborhood: str = Field(..., description="Name of the neighborhood")
    price: int = Field(..., description="Listing price in whole US dollars")
    bedrooms: int = Field(..., description="Number of bedrooms (1-6)")
    bathrooms: int = Field(..., description="Number of bathrooms (1-4)")
    house_size: str = Field(..., description='Living area, e.g. "2150 sqft"')
    description: str = Field(
        ..., description="5–6 engaging sentences describing the property"
    )
    neighborhood_description: str = Field(
        ..., description="3–4 sentences describing the neighborhood"
    )
