from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from dependencies import get_db

import schemas
from .affiliate_climate_change_impact_router import post_affiliate_climate_change_impact
from gateway.squarespace_service import calculator_create, calculator_update
from gateway import webhook_schemas


router = APIRouter(
    prefix="/calculator",
    tags=["calculator"],
    dependencies=[Depends(get_db)]
)


# once an order is created, return climate impact and update DB
# TODO: write unit test
@router.post("/order", response_model=schemas.AffiliateClimateChangeImpact, responses={404: {"model":schemas.HTTPError},                                                                        418: {"model":schemas.HTTPError}})
def climate_change_calculator(webHookOrder: webhook_schemas.WebhookRequest, db: Session = Depends(get_db)):
    if webHookOrder.topic == webhook_schemas.TopicEnum.CREATE:
        climate_change_calculator_response = calculator_create(webHookOrder, db=db)
        if type(climate_change_calculator_response) == schemas.AffiliateClimateChangeImpactCreate:
            return post_affiliate_climate_change_impact(affiliateClimateChangeImpact=climate_change_calculator_response,
                                                        db=db)
        else:
            return climate_change_calculator_response
    elif webHookOrder.topic == webhook_schemas.TopicEnum.UPDATE:
        climate_change_calculator_response = calculator_update(webHookOrder, db=db)
        if type(climate_change_calculator_response) == schemas.AffiliateClimateChangeImpactCreate:
            return post_affiliate_climate_change_impact(affiliateClimateChangeImpact=climate_change_calculator_response,
                                                        db=db)
        else:
            return climate_change_calculator_response
