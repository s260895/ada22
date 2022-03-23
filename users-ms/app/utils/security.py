from models import User
from tortoise.exceptions import DoesNotExist
from utils.exceptions import unauthorized


async def authenticate_user(username: str, password: str):
    try:
        valid_user = await User.get(username=username)
    except DoesNotExist:
        raise unauthorized
    return valid_user
