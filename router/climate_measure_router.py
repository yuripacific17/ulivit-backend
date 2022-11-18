from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from dependencies import get_db

import schemas
from crud import climate_measure_crud

router = APIRouter(
    prefix="/climate-measure",
    tags=["climate-measure"],
    dependencies=[Depends(get_db)]
)


@router.get("/", response_model=list[schemas.ClimateMeasure])
def read_climate_measure_list(skip:int = 0, limit: int = 100, db: Session = Depends(get_db)):
    climate_measure_list = climate_measure_crud.get_all_climate_measures(db=db, skip=skip, limit=limit)
    return climate_measure_list


@router.get("/id={id}", response_model=schemas.ClimateMeasure, responses={404: {"model": schemas.HTTPError}})
def read_climate_measure_by_id(id: int, db: Session = Depends(get_db)):
    single_climate_measure = climate_measure_crud.get_climate_measure_by_id(db=db, id=id)
    if single_climate_measure is None:
        return JSONResponse(status_code=404, content={"ErrorType":"RecordNotFoundError",
                                                      "Description": "Climate Measure Not Found"})
    return single_climate_measure


@router.get("/sku={sku}", response_model=schemas.ClimateMeasure, responses={404: {"model": schemas.HTTPError}})
def read_climate_measure_by_sku(sku: str, db: Session = Depends(get_db)):
    single_climate_measure = climate_measure_crud.get_climate_measure_by_sku(db=db, sku=sku)
    if single_climate_measure is None:
        return JSONResponse(status_code=404, content={"ErrorType":"RecordNotFoundError",
                                                      "Description": "Climate Measure Not Found"})
    return single_climate_measure


# upsert, create climate measure if doesn't exist, otherwise create it
@router.post("/", response_model=schemas.ClimateMeasure)
def post_climate_measure(climateMeasure: schemas.ClimateMeasureCreate, db: Session = Depends(get_db)):
    if climate_measure_crud.get_climate_measure_by_sku(db=db, sku=climateMeasure.sku) is None:
        return climate_measure_crud.create_climate_measure(db=db, climateMeasure=climateMeasure)
    else:
        return climate_measure_crud.update_climate_measure_by_sku(db=db, climateMeasure=climateMeasure)


@router.delete("/id={id}")
def delete_climate_measure_by_id(id: int, db: Session = Depends(get_db)):
    return climate_measure_crud.delete_climate_measure_by_id(db=db, id=id)


@router.delete("/sku={sku}")
def delete_climate_measure_by_sku(sku: str, db: Session = Depends(get_db)):
    return climate_measure_crud.delete_climate_measure_by_sku(db=db, sku=sku)


