from sqlalchemy import delete, update
from sqlalchemy.orm import Session

import models
import schemas


# affiliate impact change crud
def create_affiliate_climate_change_impact(db: Session,
                                           affiliateClimateChangeImpact: schemas.AffiliateClimateChangeImpactCreate):
    db_affiliate = models.AffiliateClimateChangeImpact(promoCode=affiliateClimateChangeImpact.promoCode,
                                                       totalCarsOffRoad=affiliateClimateChangeImpact.totalCarsOffRoad,
                                                       totalFightingFoodWaste=affiliateClimateChangeImpact.totalFightingFoodWaste,
                                                       totalWaterSaved=affiliateClimateChangeImpact.totalWaterSaved,
                                                       totalLandUse=affiliateClimateChangeImpact.totalLandUse,
                                                       totalCholesterolSaved=affiliateClimateChangeImpact.totalCholesterolSaved)
    db.add(db_affiliate)
    db.commit()
    db.refresh(db_affiliate)
    return db_affiliate


def get_all_affiliate_climate_change_impact(db: Session, skip: int = 0, limit: int = 100):
    query = db.query(models.AffiliateClimateChangeImpact).offset(skip).limit(limit).all()
    return query


def get_affiliate_climate_change_impact_by_promo_code(db: Session, promoCode: str):
    query = db.query(models.AffiliateClimateChangeImpact) \
        .filter(models.AffiliateClimateChangeImpact.promoCode == promoCode).first()
    return query


def get_affiliate_climate_change_impact_by_id(db: Session, id: int):
    query = db.query(models.AffiliateClimateChangeImpact) \
        .filter(models.AffiliateClimateChangeImpact.id == id).first()
    return query


def delete_affiliate_climate_change_impact_by_promote_code(db: Session, promoCode: str):
    if get_affiliate_climate_change_impact_by_promo_code(db=db, promoCode=promoCode) is None:
        return "Cannot find affiliate climate change impact with given promo code"
    query = db.execute(delete(models.AffiliateClimateChangeImpact)
                       .where(models.AffiliateClimateChangeImpact.promoCode == promoCode))
    db.commit()
    return "Successfully deleted Affiliate climate change impact"


def delete_affiliate_climate_change_impact_by_id(db: Session, id: int):
    if get_affiliate_climate_change_impact_by_id(db=db, id=id) is None:
        return "Cannot find affiliate climate change impact with given id"
    query = db.execute(delete(models.AffiliateClimateChangeImpact)
                       .where(models.AffiliateClimateChangeImpact.id == id))
    db.commit()
    return "Successfully deleted Affiliate climate change impact"


def update_affiliate_climate_change_impact_by_promote_code(db: Session,
                                                           affiliateClimateChangeImpact: schemas.AffiliateClimateChangeImpactCreate):
    db.execute(update(models.AffiliateClimateChangeImpact).where(
        models.AffiliateClimateChangeImpact.promoCode == affiliateClimateChangeImpact.promoCode)
               .values(promoCode=affiliateClimateChangeImpact.promoCode,
                       totalCarsOffRoad=affiliateClimateChangeImpact.totalCarsOffRoad,
                       totalFightingFoodWaste=affiliateClimateChangeImpact.totalFightingFoodWaste,
                       totalWaterSaved=affiliateClimateChangeImpact.totalWaterSaved,
                       totalLandUse=affiliateClimateChangeImpact.totalLandUse,
                       totalCholesterolSaved=affiliateClimateChangeImpact.totalCholesterolSaved))
    db.commit()
    return get_affiliate_climate_change_impact_by_promo_code(db=db, promoCode=affiliateClimateChangeImpact.promoCode)