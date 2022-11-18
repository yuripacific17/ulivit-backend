from fastapi.testclient import TestClient
from sqlalchemy import create_engine, schema, MetaData
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy_utils import database_exists, create_database
from dependencies import get_db

from main import app

# set up test database for unit testing
SQLALCHEMY_DATABASE_URL = "postgresql://postgres:postgres@localhost/ulivit"
SQLALCHEMY_SCHEMA_NAME = "CCC"


# create database if doesn't exist
def validate_database():
    if not database_exists(SQLALCHEMY_DATABASE_URL):
        create_database(SQLALCHEMY_DATABASE_URL)
    return None


validate_database()

engine = create_engine(
    SQLALCHEMY_DATABASE_URL
)

# create schema if doesn't exist
if not engine.dialect.has_schema(engine, SQLALCHEMY_SCHEMA_NAME):
    engine.execute(schema.CreateSchema(SQLALCHEMY_SCHEMA_NAME))
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
Base.metadata.create_all(bind=engine)

# override database config and point to test db
def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)


# create climate measure, and retrieve it to see if it exists
def test_create_and_get_climate_measure():
    response = client.post(
        "/climate-measure/",
        json={
        "sku": "DSVNI130",
        "carsOffRoad": 1.4,
        "fightingFoodWaste": 0.2,
        "waterSaved": 15,
        "landUse": 0.5,
        "cholesterolSaved": 98
        }
    )
    assert response.status_code == 200, response.text
    data = response.json()
    assert data["sku"] == "DSVNI130"
    assert "cholesterolSaved" in data
    climate_measure_id = data["id"]

    response = client.get(f"/climate-measure/id={climate_measure_id}")
    assert response.status_code == 200, response.text
    data = response.json()
    assert data["carsOffRoad"] == 1.4
    assert data["id"] == climate_measure_id


# delete the climate measure and retrieve tp see if it exists
def test_delete_climate_measure_by_sku():
    response = client.delete("/climate-measure/sku=DSVNI130")
    assert response.status_code == 200, response.text

    response = client.get("/climate-measure/sku=DSVNI130")
    assert response.status_code == 404, response.text
    data = response.json()
    assert data["ErrorType"] == "RecordNotFoundError"
    assert data["Description"] == "Climate Measure Not Found"


# create affiliate, and retrieve it to see if it exists
def test_create_affiliate():
    response = client.post(
        "/affiliate/",
        json= {
            "promoCode": "XWSA25",
            "organizationName": "The Cat Lovers",
            "emailAddress": "catlovers20221012@invalidemail.com"
        }
    )
    assert response.status_code == 200, response.text
    data = response.json()
    assert data["promoCode"] == "XWSA25"
    assert data["emailAddress"] == "catlovers20221012@invalidemail.com"
    assert data["organizationName"] == "The Cat Lovers"


# delete affiliate, and retrieve it to see if it exists
def test_delete_affiliate_by_promoCode():
    response = client.delete("/affiliate/promoCode=XWSA25")
    assert response.status_code == 200, response.text

    response = client.get("/affiliate/promoCode=XWSA25")
    data = response.json()
    assert data["ErrorType"] == "RecordNotFoundError"
    assert data["Description"] == "Affiliate Not Found"


def test_create_affiliate_climate_measure_change_impact():
    response = client.post(
        "/affiliate-climate-change-impact/",
        json={
            "promoCode": "XWSA25",
            "totalCarsOffRoad": 429,
            "totalFightingFoodWaste": 4344,
            "totalWaterSaved":9289,
            "totalLandUse": 7128,
            "totalCholesterolSaved": 1487
        }
    )

    assert response.status_code == 200, response.text
    data = response.json()
    assert data["promoCode"] == "XWSA25"
    assert data["totalCholesterolSaved"] == 1487


# delete affiliate climate change impact, and retrieve it to see if it exists
def test_delete_affiliate_climate_change_impact_by_promoCode():
    response = client.delete("/affiliate-climate-change-impact/promoCode=XWSA25")
    assert response.status_code == 200, response.text

    response = client.get("/affiliate-climate-change-impact/promoCode=XWSA25")
    data = response.json()
    assert data["ErrorType"] == "RecordNotFoundError"
    assert data["Description"] == "Affiliate Climate Change Impact Not Found"


test_create_and_get_climate_measure()
test_delete_climate_measure_by_sku()
test_create_affiliate()
test_create_affiliate_climate_measure_change_impact()
test_delete_affiliate_climate_change_impact_by_promoCode()
test_delete_affiliate_by_promoCode()

