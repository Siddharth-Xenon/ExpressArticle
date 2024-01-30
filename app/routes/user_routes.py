from fastapi import APIRouter, HTTPException, Depends, status
from fastapi.security import OAuth2PasswordRequestForm
from schemas import user_schema
from dependencies import auth, database
from models import user_model

router = APIRouter()


@router.post("/register", response_model=user_schema.UserPublic)
async def register_user(user: user_schema.UserCreate):
    print("registering")
    # Hash the user password
    hashed_password = auth.get_password_hash(user.password)

    # Exclude unset fields and add hashed password
    user_data = user.dict(exclude_unset=True)
    user_data['hashed_password'] = hashed_password

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
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
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
    return {"access_token": access_token, "token_type": "bearer"}


@router.put("/{user_id}", response_model=user_schema.UserPublic)
async def update_user_profile(user_id: str, user_update: user_schema.UserUpdate, current_user: user_schema.UserPublic = Depends(auth.get_current_user)):
    # Here, add logic to ensure that the current user is allowed to update the specified user profile
    if current_user.id != user_id:
        raise HTTPException(
            status_code=403, detail="Not authorized to update this user's profile")

    updated_user_data = user_update.dict(exclude_unset=True)
    if 'password' in updated_user_data:
        updated_user_data['hashed_password'] = auth.get_password_hash(
            updated_user_data.pop('password'))

    update_result = database.update_user(user_id, updated_user_data)
    if not update_result:
        raise HTTPException(
            status_code=404, detail="User not found or update failed")

    return {**updated_user_data, "id": user_id}
# You can add more routes for other user-related functionalities
