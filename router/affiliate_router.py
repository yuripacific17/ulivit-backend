from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from dependencies import get_db


import schemas
from crud import affiliate_crud


router = APIRouter(
    prefix="/affiliate",
    tags=["affiliate"],
    dependencies=[Depends(get_db)]
)


# upsert, create affiliate if doesn't exist, otherwise create it
@router.post("/", response_model=schemas.Affiliate)
def post_affiliate(affiliate: schemas.AffiliateCreate, db: Session = Depends(get_db)):
    if affiliate_crud.get_affiliate_by_email(db=db, emailAddress=affiliate.emailAddress) is None:
        return affiliate_crud.create_affiliate(db=db, affiliate=affiliate)
    else:
        return JSONResponse(status_code=404, content={"ErrorType": "RecordNotFoundError",
                                                      "Description": "Affiliate With the Same Email Found"})


@router.put("/", response_model=schemas.Affiliate, responses={404: {"model":schemas.HTTPError}})
def update_affiliate(affiliate:schemas.Affiliate, db: Session = Depends(get_db)):
    if affiliate_crud.get_affiliate_by_id(db=db, id=affiliate.id) is None:
        return JSONResponse(status_code=404, content={"ErrorType": "RecordNotFoundError",
                                                      "Description": "Affiliate Not Found"})
    else:
        return affiliate_crud.update_affiliate_by_id(db=db, affiliate=affiliate)


@router.get("/", response_model=list[schemas.Affiliate])
def read_affiliate_list(skip:int = 0, limit: int = 100, db: Session = Depends(get_db)):
    affiliate_list = affiliate_crud.get_all_affiliates(db=db, skip=skip, limit=limit)
    return affiliate_list


@router.get("/promoCode={promoCode}", response_model=schemas.Affiliate, responses={404: {"model":schemas.HTTPError}})
def read_affiliate_by_promo_code(promoCode: str, db: Session = Depends(get_db)):
    single_affiliate = affiliate_crud.get_affiliate_by_promo_code(db=db, promoCode=promoCode)
    if single_affiliate is None:
        return JSONResponse(status_code=404, content={"ErrorType": "RecordNotFoundError",
                                                      "Description": "Affiliate Not Found"})
    return single_affiliate


@router.get("/id={id}", response_model= schemas.Affiliate, responses={404: {"model":schemas.HTTPError}})
def read_affiliate_by_id(id: int, db: Session = Depends(get_db)):
    single_affiliate = affiliate_crud.get_affiliate_by_id(db=db, id=id)
    if single_affiliate is None:
        return JSONResponse(status_code=404, content={"ErrorType": "RecordNotFoundError",
                                                      "Description": "Affiliate Not Found"})
    return single_affiliate


@router.get("/email={emailAddress}", response_model=schemas.Affiliate, responses={404: {"model":schemas.HTTPError}})
def read_affiliate_by_email(emailAddress: str, db: Session = Depends(get_db)):
    single_affiliate = affiliate_crud.get_affiliate_by_email(db=db, emailAddress=emailAddress)
    if single_affiliate is None:
        return JSONResponse(status_code=404, content={"ErrorType": "RecordNotFoundError",
                                                      "Description": "Affiliate Not Found"})
    return single_affiliate


@router.delete("/promoCode={promoCode}")
def delete_affiliate_by_promo_code(promoCode: str, db: Session = Depends(get_db)):
    return affiliate_crud.delete_affiliate_by_promote_code(db=db, promoCode=promoCode)


@router.delete("/id={id}")
def delete_affiliate_by_id(id: int, db: Session = Depends(get_db)):
    return affiliate_crud.delete_affiliate_by_id(db=db, id=id)


@router.get("/validate/email={emailAddress}", response_model=schemas.HTTPValidation, responses={404: {"model":schemas.HTTPError}})
def validate_affiliate_by_email(emailAddress:str, db: Session = Depends(get_db)):
    single_affiliate = affiliate_crud.get_affiliate_by_email(db=db, emailAddress=emailAddress)
    if single_affiliate is None:
        return JSONResponse(status_code=200, content={"Response": "No Duplicate Found"})
    else:
        return JSONResponse(status_code=404, content={"ErrorType": "DuplicateRecord",
                                                      "Description": "Affiliate With This Email Already Exists"})


@router.put("/approve", response_model=schemas.Affiliate, responses={404: {"model":schemas.HTTPError}})
def approve_affiliate_by_id(idJson: schemas.AffiliateApprove, db: Session = Depends(get_db)):
    if affiliate_crud.get_affiliate_by_id(db=db, id=idJson.id) is None:
        return JSONResponse(status_code=404, content={"ErrorType": "RecordNotFoundError",
                                                      "Description": "Affiliate Not Found"})
    else:
        return affiliate_crud.approve_pending_affiliate_by_id(db=db, id=idJson.id)
