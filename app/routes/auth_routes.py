from fastapi import APIRouter, HTTPException, Depends, status
from fastapi.security import OAuth2PasswordRequestForm
from schemas import user_schema
from dependencies import auth, database
from models import user_model

router = APIRouter()


@router.post("/register", response_model=user_schema.UserPublic)
async def register_user(user: user_schema.UserCreate):
    # Hash the user password
    hashed_password = auth.get_password_hash(user.password)

    # Exclude unset fields, remove plain password, and add hashed password
    user_data = user.dict(exclude_unset=True)
    del user_data['password']  # Remove the plain password
    user_data['hashed_password'] = hashed_password

    existing_user = database.get_user_by_id(
        database.get_user_id(user_data["username"]))
    if existing_user:
        raise HTTPException(
            status_code=400, detail="User already exists")

    # Create a new user in the database
    new_user_id = database.create_user(user_data)
    if new_user_id is None:
        raise HTTPException(
            status_code=400, detail="Error in user registration")

    # Prepare the response data
    response_data = user_data.copy()
    response_data.update({"id": new_user_id})
    del response_data['hashed_password']

    return response_data


@router.post("/login", response_model=user_schema.Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()) -> user_schema.Token:
    print(form_data)
    user_id = database.get_user_id(form_data.username)
    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    user = database.get_user_by_id(user_id)
    if not auth.verify_password(form_data.password, user["hashed_password"]):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token = auth.create_access_token(data={"sub": user["username"]})
    return user_schema.Token(access_token=access_token, token_type="bearer")
