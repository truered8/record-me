from pydantic import BaseModel
from uuid import UUID


class TesterDto(BaseModel):
    """A model of a tester."""
    username: str
    age: int
    industry: str


class CompanyDto(BaseModel):
    """A model of a company."""
    name: str
    email: str


class ProductDto(BaseModel):
    """A model of a product."""
    company_id: UUID
    name: str
    description: str
    hourly: float
    target_age: int
    target_industry: str


class ReviewDto(BaseModel):
    """A model of a review."""
    tester_id: UUID
    product_id: UUID
    rating: float
    feedback: str
