from typing import Callable
from uuid import uuid4 as uuid
from flask import Flask, request, jsonify
from sqlalchemy.engine import Engine
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
import os

from db import CockroachService
from models import *
from prediction import CohereService

Session = sessionmaker()
app = Flask(__name__)


def get_endpoint_loader(database: CockroachService, predictor: CohereService) -> Callable[[Engine], None]:
    def init_endpoints(engine: Engine):
        Session.configure(bind=engine)

        @app.post("/review/")
        def add_review():
            new_review = Review(
                id=uuid(),
                tester_id=request.json.get("tester_id"),
                product_id=request.json.get("product_id"),
                rating=request.json.get("rating"),
                feedback=request.json.get("feedback")
            )
            session = Session()
            response = {}
            try:
                label = predictor.get_categories(new_review.feedback)
                response.update({"label": label})
                product = database.get_product(session, str(new_review.product_id))
                if label in product.issues:
                    product.issues[label] += 1
                else:
                    product.issues[label] = 1

                database.update_product(session, product)
                session.commit()
            except:
                print("Couldn't categorize review.")

            try:
                database.add_review(session, new_review)
                session.commit()
                response.update({"review_id": new_review.id})
                return jsonify(response)
            except:
                return "Couldn't add review in database."

        @app.get("/review/")
        def get_reviews():
            session = Session()
            try:
                res = database.get_reviews(session, request.args.get("product_id"))
                return [{"id": r.id, "rating": r.rating, "feedback": r.feedback} for r in res]
            except:
                return "Couldn't read reviews table."

        @app.post("/product/")
        def add_product():
            new_product = Product(
                id=uuid(),
                company_id=request.json.get("product_id"),
                name=request.json.get("name"),
                description=request.json.get("description"),
                hourly=request.json.get("hourly"),
                target_age=request.json.get("target_age"),
                target_industry=request.json.get("target_industry"),
                issues={}
            )
            session = Session()
            try:
                database.add_product(session, new_product)
                session.commit()
                return {"product_id": new_product.id}
            except:
                return "Couldn't add product in database."

        @app.get("/product/")
        def get_products():
            session = Session()
            try:
                res = database.get_products(session, request.args.get("company_id"))
                return [{"id": r.id, "name": r.name, "issues": r.issues} for r in res]
            except:
                return "Couldn't read product table."

        @app.get("/matches/")
        def get_matches():
            session = Session()
            try:
                res = database.get_matched_products(session, request.args.get("tester_id"))
                return [{"id": r.id, "name": r.name, "issues": r.issues} for r in res]
            except:
                return "Couldn't read product table."

        @app.post("/tester/")
        def add_tester():
            new_tester = Tester(
                id=uuid(),
                username=request.json.get("username"),
                industry=request.json.get("industry"),
                age=request.json.get("age")
            )
            session = Session()
            try:
                database.add_tester(session, new_tester)
                session.commit()
                return {"tester_id": new_tester.id}
            except:
                return "Couldn't add tester in database."

        @app.post("/company/")
        def add_company():
            new_company = Company(
                id=uuid(),
                name=request.json.get("name"),
                email=request.json.get("email")
            )
            session = Session()
            try:
                database.add_company(session, new_company)
                session.commit()
                return {"company_id": new_company.id}
            except:
                return "Couldn't add company in database."

    return init_endpoints


def run_app():
    database = CockroachService()
    predictor = CohereService()
    database.connect(get_endpoint_loader(database, predictor))

    load_dotenv()
    return app


if __name__ == "__main__":
    run_app()

