from models.user import User, Gender, Role
from uuid import uuid4
from typing import List

def get_users():
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
         roles=[Role.admin,Role.user]
    )
]
    return db