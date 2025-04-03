from typing import List
from dotenv import load_dotenv
import os

load_dotenv()


def verify_password(plain_password:str, hashed_password: str):
    return plain_password == hashed_password


def parse_roles(roles_str: str) -> List[str]:
    return [role.strip() for role in roles_str.split(",") if role.strip()]





