import os
from typing import Callable
from dotenv import load_dotenv
from sqlalchemy import create_engine, update
from sqlalchemy.orm import Session
from sqlalchemy.engine import Engine

from models import *


class CockroachService:
    @staticmethod
    def connect(callback: Callable[[Engine], None]) -> None:
        """Connects to the database."""
        engine = create_engine(os.getenv("DATABASE_URL"))
        Base.metadata.create_all(engine)
        print("Connected to database.")
        callback(engine)

    @staticmethod
    def add_review(session: Session, review: Review) -> None:
        """Adds a review to the review table."""
        session.add(review)

    @staticmethod
    def get_reviews(session: Session, product_id: str) -> "list[Review]":
        """Returns the reviews for the given product."""
        return session.query(Review).filter_by(product_id=product_id).all()

    @staticmethod
    def add_product(session: Session, product: Product) -> None:
        """Adds a product to the product table."""
        session.add(product)

    @staticmethod
    def update_product(session: Session, product: Product) -> None:
        """Updates a product in the product table."""
        session.execute(
            update(Product.__table__)
            .where(Product.__table__.c.id == product.id)
            .values(issues=product.issues)
        )

    @staticmethod
    def get_product(session: Session, product_id: str) -> Product:
        """Returns the product with the given id."""
        return session.query(Product).filter_by(id=product_id).first()

    @staticmethod
    def get_products(session: Session, company_id: str) -> "list[Product]":
        """Returns the products of the given company."""
        return session.query(Product).filter_by(company_id=company_id).all()

    @staticmethod
    def get_matched_products(session: Session, tester_id: str) -> "list[Product]":
        """Returns the products matched with a given tester."""
        tester = session.query(Tester).filter_by(id=tester_id).first()
        products = session.query(Product).all()

        def compare(p: Product) -> int:
            diff = abs(p.target_age - tester.age)
            if p.target_industry != tester.industry:
                diff += 1000
            return diff

        return sorted(products, key=compare)

    @staticmethod
    def add_tester(session: Session, tester: Tester) -> None:
        """Adds a tester to the tester table."""
        session.add(tester)

    @staticmethod
    def add_company(session: Session, company: Company) -> None:
        """Adds a company to the company table."""
        session.add(company)


load_dotenv()
