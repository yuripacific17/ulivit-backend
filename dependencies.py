from database import SessionLocal


# start and get db session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()