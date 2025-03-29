from fastapi import HTTPException
from app.models.user import User, Gender, Role
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

def get_users():
    return db


def register_user(user: User):
     db.append(user)
     return {"id": user.id}


def remove_user(user_id: UUID):
     for user in db:
          if user.id == user_id:
               db.remove(user)
               return {"message": f"User with id : {user_id} deleted successfully"}
     raise HTTPException(
    status_code=404, 
    detail=f"User with id {user_id} not found")
     