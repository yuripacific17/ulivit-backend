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


@router.get("/login/username={username}&password={password}", response_model=schemas.AdminAuthentication, responses={404: {"model": schemas.HTTPError}})
def admin_login(username: str, password: str, db: Session = Depends(get_db)):
    if admin_crud.login_by_username(db=db, username=username, password=password) is None:
        return JSONResponse(status_code=404, content={"authResult":"Username and password not found"})
    else:
        return JSONResponse(status_code=200, content={"authResult":"Authentication Successful"})


@router.post("/id={id}", response_model=schemas.Admin)
def update_admin(admin: schemas.AdminCreate, id: int, db: Session = Depends(get_db)):
    return admin_crud.update_admin_by_id(db=db, admin=admin, id=id)