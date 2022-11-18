from fastapi import FastAPI

from router import admin_router, affiliate_climate_change_impact_router, affiliate_router, calculator_router, \
    climate_measure_router

app = FastAPI()


@app.get("/", tags=["Root"])
async def read_root() -> dict:
    return {
        "message": "Welcome to ulivit IMPACT calculator, use the /docs route to proceed"
    }


app.include_router(admin_router.router)
app.include_router(affiliate_climate_change_impact_router.router)
app.include_router(affiliate_router.router)
app.include_router(calculator_router.router)
app.include_router(climate_measure_router.router)

