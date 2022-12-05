from sqlalchemy import delete, update
from sqlalchemy.orm import Session

import models
import schemas


# authenticate admin users
def create_admin(db: Session, admin: schemas.AdminCreate):
    db_admin = models.Admin(emailAddress=admin.emailAddress, username=admin.username, password=admin.password)
    db.add(db_admin)
    db.commit()
    db.refresh(db_admin)

    return db_admin


def update_admin_by_id(db: Session, admin: schemas.AdminCreate, id: int):
    if get_admin_by_id(db=db, id=id) is None:
        return "Cannot find this admin account"
    else:
        db.execute(update(models.Admin).where(models.Admin.id == id)
                   .values(emailAddress=admin.emailAddress, username=admin.username, password=admin.password))
        db.commit()
        return get_admin_by_id(db=db, id=id)


def login_by_username(db: Session, username: str, password: str):
    query = db.query(models.Admin).filter(models.Admin.username == username, models.Admin.password == password).first()

    return query


def get_admin_by_username(db: Session, username: str):
    query = db.query(models.Admin).filter(models.Admin.username == username).first()

    return query


def get_admin_by_email(db: Session, emailAddress: str):
    query = db.query(models.Admin).filter(models.Admin.emailAddress == emailAddress).first()

    return query


def get_admin_by_id(db: Session, id: int):
    query = db.query(models.Admin).filter(models.Admin.id == id).first()

    return query


def get_all_admins(db: Session, skip: int = 0, limit: int = 100):
    query = db.query(models.Admin).offset(skip).limit(limit).all()
    return query


def delete_admin_by_id(db:Session, id: int):
    if get_admin_by_id(db=db, id=id) is None:
        return "Cannot find admin with given id"
    query = db.execute(delete(models.Admin).where(models.Admin.id == id))
    db.commit()
    return "Successfully deleted Admin"

def delete_admin_by_username(db: Session, username: str):
    if get_admin_by_username(db=db, username=username) is None:
        return "Cannot find admin with given username"
    query = db.execute(delete(models.Admin).where(models.Admin.username == username))
    db.commit()
    return "Successfully deleted Admin"


def delete_admin_by_email(db: Session, email: str):
    if get_admin_by_email(db=db, emailAddress=email) is None:
        return "Cannot find admin with given email"
    query = db.execute(delete(models.Admin).where(models.Admin.emailAddress == email))
    db.commit()
    return "Successfully deleted Admin"