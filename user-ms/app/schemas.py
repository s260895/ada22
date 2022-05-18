import models
from pydantic import BaseModel
from tortoise.contrib.pydantic import pydantic_model_creator


UserIn_Pydantic = pydantic_model_creator(
    models.User, name="UserIn", include=(
        "username", "password",
    )
)
UserOut_Pydantic = pydantic_model_creator(
    models.User, name="UserOut", include=(
        "id", "username",
    )
)


class Status(BaseModel):
    message: str
