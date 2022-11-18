from sqlalchemy import delete, update
from sqlalchemy.orm import Session
from uuid import uuid4

import models
import schemas


def create_affiliate_status(db: Session, affiliateStatus: schemas.AffiliateStatusCreate):
    db_affiliate_status = models.AffiliateStatus(id=uuid4(), status=affiliateStatus.status)
    db.add(db_affiliate_status)
    db.commit()
    db.refresh(db_affiliate_status)
    return db_affiliate_status


def get_all_affiliate_status(db: Session, skip: int = 0, limit: int = 100):
    query = db.query(models.AffiliateStatus).offset(skip).limit(limit).all()
    return query


def get_affiliate_status_by_id(db: Session, id: str):
    query = db.query(models.AffiliateStatus).filter(models.AffiliateStatus.id == id).first()
    return query


def delete_affiliate_status_by_id(db: Session, id: str):
    if get_affiliate_status_by_id(db=db, id=id) is None:
        return "Cannot find affiliate with given promo code"
    query = db.execute(delete(models.AffiliateStatus).where(models.AffiliateStatus.id == id))
    db.commit()
    return "Successfully deleted Affiliate"
