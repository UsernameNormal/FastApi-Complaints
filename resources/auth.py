from lib2to3.pgen2 import token
from fastapi import APIRouter
from managers.user import UserManager
from schemas.request.user import UserLogIn, UserRegisterIn

router = APIRouter(tags=["Auth"])


@router.post("/register/", status_code=201)
async def register(user_data: UserRegisterIn):

    token = await UserManager.register(user_data.dict())
    return {"token": token}


@router.post("/login/", status_code=200)
async def login(user_data: UserLogIn):

    token = await UserManager.login(user_data.dict())
    return {"token": token}
