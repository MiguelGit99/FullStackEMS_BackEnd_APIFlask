from apiflask import abort
import jwt
from sqlalchemy import select
from sqlalchemy.orm import joinedload
from blueprints.auth.schemas import ChangePasswordSchema, LoginSchema, UserResponseSchema
from core.extensions import db
from blueprints.auth.models import User
from core.decorators import log

#@log
def verify_login(login: LoginSchema):

    stmt = (
        select(User)
        .options(joinedload(User.employee))
        .where(User.email == login.email)
        # .scalar_one_or_none()
    )

    user = db.session.execute(stmt).scalar_one_or_none()

    if (user is None or not user.verify_password(login.password)):
        abort(401, "Invalid email or password")

    return user



def update_password(user_id: int, data: ChangePasswordSchema):
    if (data is None):
        abort(401, "Both passwords required.")
    
    stmt = (
        select(User)
        .where(
            User.id == user_id
        )
    )

    db_user = db.session.execute(stmt).scalar_one_or_none()

    # update_data = db_user.model_dump(
    #     exclude_unset=True
    # )
    
    if db_user is None:
        abort(404, description="Invalid session or user not found")

    if (db_user is None or not db_user.verify_password(data.currentPassword)):
        abort(401, "Invalid password")

    #update_data.hash_password(data.newPassword)
    db_user.hash_password(data.newPassword)

    # user_schema = UserResponseSchema (
    #     id=user.id,
    #     email=user.email,
    #     role=user.role
    # )

    db.session.commit()
    db.session.refresh(db_user)

    



