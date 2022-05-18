from models import User
from schemas import UserOut_Pydantic, UserIn_Pydantic, Status
from fastapi import APIRouter
from tortoise.contrib.fastapi import HTTPNotFoundError
from tortoise.exceptions import DoesNotExist
from utils.exceptions import not_found


user_router = APIRouter(tags=["users"])


"""User endpoints"""
@user_router.post("/users", response_model=UserOut_Pydantic, description="Register a new user.")
async def register(user: UserIn_Pydantic):
    new_user = await User.create(**user.dict(exclude_unset=True))
    return await UserOut_Pydantic.from_tortoise_orm(new_user)


@user_router.put("/users/{user_id}", response_model=UserOut_Pydantic, responses={404: {"model": HTTPNotFoundError}}, description="Update a user.")
async def update_user(user_id: int, updated_user: UserIn_Pydantic):
    await User.filter(id=user_id).update(**updated_user.dict(exclude_unset=True))

    try:
        user = User.get(id=user_id)
    except DoesNotExist:
        raise not_found

    return await UserOut_Pydantic.from_queryset_single(user)


@user_router.delete("/users/{user_id}", response_model=Status, responses={404: {"model": HTTPNotFoundError}}, description="Delete a user.")
async def delete_user(user_id: int):
    user_delete = await User.filter(id=user_id).delete()

    if not user_delete:
        raise not_found

    return Status(message=f"User {user_id} was deleted")
