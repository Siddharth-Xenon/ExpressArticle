from fastapi import APIRouter, HTTPException, Depends, status
from fastapi.security import OAuth2PasswordRequestForm
from schemas import user_schema
from dependencies import auth, database
from models import user_model

router = APIRouter()


@router.put("/", response_model=user_schema.UserPublic)
async def update_user_profile(user_update: user_schema.UserUpdate, current_user: user_schema.UserPublic = Depends(auth.get_current_user)):
    # Here, add logic to ensure that the current user is allowed to update the specified user profile
    user_id = current_user["_id"]
    if current_user["_id"] != user_id:
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
    user = database.get_user_by_id(user_id)
    return {**user, "id": user_id}
# You can add more routes for other user-related functionalities
