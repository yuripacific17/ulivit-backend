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


def get_all_admin(db: Session, skip: int = 0, limit: int = 100):
    pass


def delete_admin_by_id(db:Session, id: int):
    pass


def delete_admin_by_username(db: Session, username: str):
    pass


def delete_admin_by_email(db: Session, email: str):
    pass