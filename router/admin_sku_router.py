from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from dependencies import get_db

import schemas
from crud import climate_measure_crud
from gateway import squarespace_service

router = APIRouter(
    prefix="/admin_sku",
    tags=["admin_sku"],
    dependencies=[Depends(get_db)]
)


@router.get("/", response_model=list[schemas.ClimateMeasure])
def read_climate_measure_list(skip:int = 0, limit: int = 100, db: Session = Depends(get_db)):
    squarespace_service.fetch_sku_for_admin (db=db, skip=skip, limit=limit)
    climate_measure_list = climate_measure_crud.get_all_climate_measures(db=db, skip=skip, limit=limit)
    return climate_measure_list


