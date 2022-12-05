from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from dependencies import get_db

import schemas
from crud import admin_crud


router = APIRouter(
    prefix="/admin",
    tags=["admin"],
    dependencies=[Depends(get_db)]
)


@router.post("/", response_model=schemas.Admin)
def create_admin(admin: schemas.AdminCreate, db: Session = Depends(get_db)):
    return admin_crud.create_admin(db=db, admin=admin)

@router.get("/", response_model=list[schemas.Admin])
def read_admin_list(skip:int = 0, limit: int = 100, db: Session = Depends(get_db)):
    admin_list = admin_crud.get_all_admins(db=db, skip=skip, limit=limit)
    return admin_list

@router.get("/login/username={username}&password={password}", response_model=schemas.AdminAuthentication, responses={404: {"model": schemas.HTTPError}})
def admin_login(username: str, password: str, db: Session = Depends(get_db)):
    if admin_crud.login_by_username(db=db, username=username, password=password) is None:
        return JSONResponse(status_code=404, content={"authResult":"Username and password not found"})
    else:
        return JSONResponse(status_code=200, content={"authResult":"Authentication Successful"})


@router.post("/id={id}", response_model=schemas.Admin)
def update_admin(admin: schemas.AdminCreate, id: int, db: Session = Depends(get_db)):
    return admin_crud.update_admin_by_id(db=db, admin=admin, id=id)

@router.delete("/id={id}")
def delete_admin_by_id(id: int, db: Session = Depends(get_db)):
    return admin_crud.delete_admin_by_id(db=db, id=id)

@router.delete("/username={username}")
def delete_admin_by_username(username: str, db: Session = Depends(get_db)):
    return admin_crud.delete_admin_by_username(db=db, username=username)

@router.delete("/email={email}")
def delete_admin_by_email(email: str, db: Session = Depends(get_db)):
    return admin_crud.delete_admin_by_email(db=db, email=email)
