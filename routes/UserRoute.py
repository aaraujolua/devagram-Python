from fastapi import APIRouter, Body

router = APIRouter()

@router.post("/", response_description='Route to create a new user')
async def route_create_new_user(user = Body(...)):
    return {
        "Msg": "User successfully registered!"
    }