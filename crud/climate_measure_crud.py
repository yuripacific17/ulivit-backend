from sqlalchemy import delete, update
from sqlalchemy.orm import Session

import models
import schemas


# climate crud
def create_climate_measure(db: Session, climateMeasure: schemas.ClimateMeasureCreate):
    db_climateMeasure = models.ClimateMeasure(sku=climateMeasure.sku, carsOffRoad=climateMeasure.carsOffRoad,
                                              fightingFoodWaste=climateMeasure.fightingFoodWaste,
                                              waterSaved=climateMeasure.waterSaved, landUse=climateMeasure.landUse,
                                              cholesterolSaved=climateMeasure.cholesterolSaved)
    db.add(db_climateMeasure)
    db.commit()
    db.refresh(db_climateMeasure)
    return db_climateMeasure


def get_all_climate_measures(db: Session, skip: int = 0, limit: int = 100):
    query = db.query(models.ClimateMeasure).offset(skip).limit(limit).all()
    return query


def get_climate_measure_by_id(db: Session, id: int):
    query = db.query(models.ClimateMeasure).filter(models.ClimateMeasure.id == id).first()
    return query


def get_climate_measure_by_sku(db: Session, sku: str):
    query = db.query(models.ClimateMeasure).filter(models.ClimateMeasure.sku == sku).first()
    return query


def delete_climate_measure_by_id(db: Session, id: int):
    if get_climate_measure_by_id(db=db, id=id) is None:
        return "Cannot find climate measure with given id"
    query = db.execute(delete(models.ClimateMeasure).where(models.ClimateMeasure.id == id))
    db.commit()
    return "Successfully deleted climate measure"


def delete_climate_measure_by_sku(db: Session, sku: str):
    if get_climate_measure_by_sku(db=db, sku=sku) is None:
        return "Cannot find climate measure with given SKU"
    query = db.execute(delete(models.ClimateMeasure).where(models.ClimateMeasure.sku == sku))
    db.commit()
    return "Successfully deleted climate measure"


def update_climate_measure_by_sku(db: Session, climateMeasure: schemas.ClimateMeasureCreate):
    db.execute(update(models.ClimateMeasure).where(models.ClimateMeasure.sku == climateMeasure.sku)
               .values(sku=climateMeasure.sku, carsOffRoad=climateMeasure.carsOffRoad,
                       fightingFoodWaste=climateMeasure.fightingFoodWaste,
                       waterSaved=climateMeasure.waterSaved, landUse=climateMeasure.landUse,
                       cholesterolSaved=climateMeasure.cholesterolSaved))
    db.commit()
    return get_climate_measure_by_sku(db=db, sku=climateMeasure.sku)
