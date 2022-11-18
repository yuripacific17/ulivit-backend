from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import event
import uvicorn

import models, schemas
from database import engine
from router import admin_router, affiliate_climate_change_impact_router, affiliate_router, calculator_router, climate_measure_router
from seeding import initialize_table


app = FastAPI()

origins = [
    
    "http://localhost",
    "http://localhost:8080",
    "http://localhost:3000",
    "http://impactcalculator.ulivit.ca",
    "https://impactcalculator.ulivit.ca",
    "impactcalculator.ulivit.ca"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(admin_router.router)
app.include_router(affiliate_climate_change_impact_router.router)
app.include_router(affiliate_router.router)
app.include_router(calculator_router.router)
app.include_router(climate_measure_router.router)


@app.on_event("startup")
def configure():
    models.Base.metadata.create_all(bind=engine)
    # Populate wellknown data (and test data if necessary)
    initialize_table()


if __name__ == "__main__":
  uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)

