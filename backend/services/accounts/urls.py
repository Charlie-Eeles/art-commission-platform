from fastapi import APIRouter, Depends
from pydantic import BaseModel, EmailStr

from middleware.auth import get_current_user
from services.accounts.query_functions import get_user, create_new_user

router = APIRouter()


class CreateUserRequest(BaseModel):
    email: EmailStr


@router.get("/users/me")
def get_me(
    user=Depends(get_current_user),
):
    return dict(user)
