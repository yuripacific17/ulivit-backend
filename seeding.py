from sqlalchemy.orm import Session

from wellknown import Wellknown
from database import engine
from crud import affiliate_status_crud


def initialize_test_data():
    pass


def initialize_affiliate_status():
    """
        insert affiliate status wellknown data into the db
        :param: N/A
        :return: N/A
    """
    db = Session(engine)
    wellknown = Wellknown()
    affiliate_status_orm_arr = wellknown.affiliate_status_wellknown_mapper_to_orm()
    for affiliate_status_orm in affiliate_status_orm_arr:
        if affiliate_status_crud.get_affiliate_status_by_id(db=db, id=affiliate_status_orm.id) is None:
            db.add(affiliate_status_orm)
            db.commit()
            db.refresh(affiliate_status_orm)


def initialize_table():
    """
        insert wellknown data (and test data if necessary) into the db
        :param: N/A
        :return: N/A
    """
    initialize_affiliate_status()
    initialize_test_data()