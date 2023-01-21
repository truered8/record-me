from sqlalchemy import Column, SmallInteger, String, Numeric
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class Tester(Base):
    """A model of a tester."""
    __tablename__ = 'testers'
    id = Column(UUID(as_uuid=True), primary_key=True)

    username = Column(String(200))
    age = Column(SmallInteger())
    industry = Column(String(200))

    def __repr__(self):
        return f"Tester<{self.id} | {self.username}>"


class Company(Base):
    """A model of a company."""
    __tablename__ = 'companies'
    id = Column(UUID(as_uuid=True), primary_key=True)

    name = Column(String(200))
    email = Column(String(200))

    def __repr__(self):
        return f"Company<{self.id} | {self.name}>"


class Product(Base):
    """A model of a product."""
    __tablename__ = 'products'
    id = Column(UUID(as_uuid=True), primary_key=True)

    company_id = Column(UUID(as_uuid=True), primary_key=False)
    name = Column(String(200))
    description = Column(String(500))
    hourly = Column(Numeric(10, 2))
    target_age = Column(SmallInteger())
    target_industry = Column(String(200))
    issues = Column(JSONB)

    def __repr__(self):
        return f"Product<{self.id} | {self.name}>"


class Review(Base):
    """A model of a review."""
    __tablename__ = 'reviews'
    id = Column(UUID(as_uuid=True), primary_key=True)

    tester_id = Column(UUID(as_uuid=True), primary_key=False)
    product_id = Column(UUID(as_uuid=True), primary_key=False)
    rating = Column(Numeric(10, 2))
    feedback = Column(String(2000))

    def __repr__(self):
        return f"Review<{self.id} | {self.rating}>"
