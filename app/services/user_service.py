from fastapi import HTTPException
from app.models.user import User, Gender, Role, UserUpdateRequest
from uuid import UUID, uuid4
from typing import List


db: List[User] = [
    User(id=uuid4(), 
         first_name="Jamila", 
         last_name="Adeoye",
         gender=Gender.female,
         roles=[Role.student]
    ),
    User(id=uuid4(), 
         first_name="Alex", 
         last_name="Jones",
         gender=Gender.male,
         roles=[Role.admin, Role.user]
    )
]

def get_users_db():
     return db

def get_all_users(db: List[User]):
    return db


def register_user(user: User, db: List[User]):
     db.append(user)
     return {"id": user.id}


def remove_user(user_id: UUID, db: List[User]):
     for user in db:
          if user.id == user_id:
               db.remove(user)
               return {"message": f"User with id : {user_id} deleted successfully"}
     raise HTTPException(
    status_code=404, 
    detail=f"User with id {user_id} not found")
     
     
def update_user(user_id: UUID, user_update: UserUpdateRequest, db: List[User]):
    for user in db:
        if user.id == user_id:
            if user_update.first_name:
                user.first_name = user_update.first_name
            if user_update.last_name:
                user.last_name = user_update.last_name
            if user_update.middle_name:
                user.middle_name = user_update.middle_name
            if user_update.roles:
                user.roles = user_update.roles
            return {"message": f"User with id : {user_id} updated successfully"}
    raise HTTPException(
        status_code=404, 
        detail=f"User with id {user_id} not found")
     