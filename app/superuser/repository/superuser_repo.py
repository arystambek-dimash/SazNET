from sqlalchemy.orm import Session
from sqlalchemy import delete
from ...database.models import SuperUser


class SuperUserRepo:
    @staticmethod
    def add_to_super_user(db: Session, user_id):
        super_user = SuperUser(user_id=user_id)
        db.add(super_user)
        db.commit()
        db.refresh(super_user)
        return super_user

    @staticmethod
    def get_all_super_user(db: Session):
        return db.query(SuperUser).all()

    @staticmethod
    def delete_super_user(db: Session, user_id):
        db_user = delete(SuperUser).filter(SuperUser.user_id == user_id)
        db.execute(db_user)
        db.commit()
        return db_user


super_user_repo = SuperUserRepo()
