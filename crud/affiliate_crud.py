from sqlalchemy import delete, update
from sqlalchemy.orm import Session
from uuid import uuid4

import models
import schemas
from wellknown import Wellknown

wellknown = Wellknown()


def create_affiliate(db: Session, affiliate: schemas.AffiliateCreate):
    db_affiliate = models.Affiliate(promoCode=affiliate.promoCode, organizationName=affiliate.organizationName,
                                    statusId=wellknown.affiliate_status_id_pending, emailAddress=affiliate.emailAddress)
    db.add(db_affiliate)
    db.commit()
    db.refresh(db_affiliate)
    return db_affiliate


def get_all_affiliates(db: Session, skip: int = 0, limit: int = 100):
    query = db.query(models.Affiliate).offset(skip).limit(limit).all()
    return query


def get_affiliate_by_promo_code(db: Session, promoCode: str):
    query = db.query(models.Affiliate).filter(models.Affiliate.promoCode == promoCode).first()
    return query


def get_affiliate_by_id(db: Session, id: int):
    query = db.query(models.Affiliate).filter(models.Affiliate.id == id).first()
    return query


def get_affiliate_by_email(db:Session, emailAddress: str):
    query = db.query(models.Affiliate).filter(models.Affiliate.emailAddress == emailAddress).first()
    return query


def delete_affiliate_by_promote_code(db: Session, promoCode: str):
    if get_affiliate_by_promo_code(db=db, promoCode=promoCode) is None:
        return "Cannot find affiliate with given promo code"
    query = db.execute(delete(models.Affiliate).where(models.Affiliate.promoCode == promoCode))
    db.commit()
    return "Successfully deleted Affiliate"


def delete_affiliate_by_id(db: Session, id: int):
    if get_affiliate_by_id(db=db, id=id) is None:
        return "Cannot find affiliate with given id"
    query = db.execute(delete(models.Affiliate).where(models.Affiliate.id == id))
    db.commit()
    return "Successfully deleted Affiliate"


def update_affiliate_by_id(db: Session, affiliate: schemas.Affiliate):
    db.execute(update(models.Affiliate).where(models.Affiliate.id == affiliate.id)
               .values(promoCode=affiliate.promoCode, organizationName=affiliate.organizationName,
                       emailAddress=affiliate.emailAddress))
    db.commit()
    return get_affiliate_by_id(db=db, id=affiliate.id)


def update_affiliate_by_email_address(db: Session, affiliate: schemas.Affiliate):
    db.execute(update(models.Affiliate).where(models.Affiliate.emailAddress == affiliate.emailAddress)
               .values(promoCode=affiliate.promoCode, organizationName=affiliate.organizationName,
                       emailAddress=affiliate.emailAddress))
    db.commit()
    return get_affiliate_by_email(db=db, emailAddress=affiliate.emailAddress)


def update_affiliate_by_promote_code(db: Session, affiliate: schemas.AffiliateCreate):
    db.execute(update(models.Affiliate).where(models.Affiliate.promoCode == affiliate.promoCode)
               .values(promoCode=affiliate.promoCode, organizationName=affiliate.organizationName,
                       emailAddress=affiliate.emailAddress))
    db.commit()
    return get_affiliate_by_promo_code(db=db, promoCode=affiliate.promoCode)


def approve_pending_affiliate_by_id(db:Session, id: int):
    db.execute(update(models.Affiliate).where(models.Affiliate.id == id)
               .values(statusId=wellknown.affiliate_status_id_approved))
    db.commit()
    return get_affiliate_by_id(db=db, id=id)


def get_associated_affiliate_promo_code_from_list(db: Session,
                                                  promo_codes: list):
    """
    Gets the promo code associated with an affiliate.\n
    Note: If there are multiple valid affiliate promo codes, the oldest affiliate will be selected.

    :param db: Session
    :param promo_codes: A list of promo codes (from an order)
    :return: A promo code string for an affiliate, or None if no codes match
    """
    query = db.query(models.Affiliate.promoCode).filter(models.Affiliate.promoCode.in_(promo_codes)).first()

    if query is not None:
        return query[0]

    return None
