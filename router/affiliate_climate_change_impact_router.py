from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from dependencies import get_db

import schemas
from crud import affiliate_climate_change_impact_crud
from crud import affiliate_crud


router = APIRouter(
    prefix="/affiliate-climate-change-impact",
    tags=["affiliate-climate-change-impact"],
    dependencies=[Depends(get_db)]
)


# upsert, create affiliate climate change impact if doesn't exist, otherwise create it
@router.post("/", response_model=schemas.AffiliateClimateChangeImpact, responses={404: {"model":schemas.HTTPError}})
def post_affiliate_climate_change_impact(affiliateClimateChangeImpact: schemas.AffiliateClimateChangeImpactCreate, db: Session = Depends(get_db)):
    if affiliate_crud.get_affiliate_by_promo_code(db=db, promoCode=affiliateClimateChangeImpact.promoCode) is None:
        return JSONResponse(status_code=404, content={"ErrorType": "ForeignKeyConstraintError",
                                                      "Description": "Can't create or update affiliate climate change "
                                                                     "impact because affiliate with given promoCode "
                                                                     "is not found"})
    else:
        if affiliate_climate_change_impact_crud.get_affiliate_climate_change_impact_by_promo_code(db=db, promoCode=affiliateClimateChangeImpact.promoCode) is None:
            return affiliate_climate_change_impact_crud.create_affiliate_climate_change_impact(db=db, affiliateClimateChangeImpact=affiliateClimateChangeImpact)
        else:
            return affiliate_climate_change_impact_crud.update_affiliate_climate_change_impact_by_promote_code(db=db, affiliateClimateChangeImpact=affiliateClimateChangeImpact)


@router.get("/", response_model=list[schemas.AffiliateClimateChangeImpact])
def read_affiliate_climate_change_impact_list(skip:int = 0, limit: int = 100, db: Session = Depends(get_db)):
    affiliate_climate_change_impact_list = affiliate_climate_change_impact_crud.get_all_affiliate_climate_change_impact(db=db, skip=skip, limit=limit)
    return affiliate_climate_change_impact_list


@router.get("/promoCode={promoCode}", response_model=schemas.AffiliateClimateChangeImpact, responses={404: {"model":schemas.HTTPError}})
def read_affiliate_climate_change_impact_by_promo_code(promoCode: str, db: Session = Depends(get_db)):
    single_affiliate_climate_change_impact = affiliate_climate_change_impact_crud.get_affiliate_climate_change_impact_by_promo_code(db=db, promoCode=promoCode)
    if single_affiliate_climate_change_impact is None:
        return JSONResponse(status_code=404, content={"ErrorType": "RecordNotFoundError",
                                                      "Description": "Affiliate Climate Change Impact Not Found"})
    return single_affiliate_climate_change_impact


@router.get("/id={id}", response_model= schemas.AffiliateClimateChangeImpact, responses={404: {"model":schemas.HTTPError}})
def read_affiliate_climate_change_impact_by_id(id: int, db: Session = Depends(get_db)):
    single_affiliate_climate_change_impact = affiliate_climate_change_impact_crud.get_affiliate_climate_change_impact_by_id(db=db, id=id)
    if single_affiliate_climate_change_impact is None:
        return JSONResponse(status_code=404, content={"ErrorType": "RecordNotFoundError",
                                                      "Description": "Affiliate Climate Change Impact Not Found"})
    return single_affiliate_climate_change_impact


@router.delete("/promoCode={promoCode}")
def delete_affiliate_climate_change_impact_by_promo_code(promoCode: str, db: Session = Depends(get_db)):
    return affiliate_climate_change_impact_crud.delete_affiliate_climate_change_impact_by_promote_code(db=db, promoCode=promoCode)


@router.delete("/id={id}")
def delete_affiliate_climate_change_impact_by_id(id: int, db: Session = Depends(get_db)):
    return affiliate_climate_change_impact_crud.delete_affiliate_climate_change_impact_by_id(db=db, id=id)
