from fastapi import APIRouter, Request, HTTPException, Depends
from fastapi.templating import Jinja2Templates
from jose import jwt, JWTError, ExpiredSignatureError
import os
from dotenv import load_dotenv
from atmo_db.models import User, Audio_File
from atmo_db.database import get_session
from sqlmodel import Session, select
from fastapi.responses import RedirectResponse

load_dotenv()

router = APIRouter()
templates = Jinja2Templates(directory="templates")

# helper method to check for valid jwt token ------------------------------------------------
def authorise_access(request: Request):
    jwt_token = request.cookies.get('auth_token')
    if not jwt_token:
        raise HTTPException(status_code=401, detail='401 Unauthorised')
    
    try:
        KEY = os.getenv("SECRET")
        ALGORITHM = os.getenv("ALGORITM")

        payload = jwt.decode(jwt_token, KEY, ALGORITHM)
        return payload
    
    except ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="401 Unauthorised: Session Expired")
    except JWTError:
        raise HTTPException(status_code=401, detail="401 Unauthorised: Invalid Token")
    
    

# routes protected with authorisation ---------------------------------------------------------
@router.get("/admin-area/{user_id}")
async def list_users(request: Request,
                     user_id: int, 
                     token_decoded_data: dict = Depends(authorise_access),
                     session: Session = Depends(get_session)):
    
    # if authorised get data for that user
    #look up user from db and pass their data into the reponse
    token_user_id = token_decoded_data['id']

    if token_user_id != user_id:
        raise HTTPException(status_code=401, detail="401 Unauthorised Access")
    
    statement = select(User).where(User.id == token_user_id)
    user = session.exec(statement).first()

    role = user.role
    username = user.username

    if role not in ['admin', 'owner']:
        raise HTTPException(status_code=401, detail="403 Forbidden")
    
    # if authorised then get 10
    users_dict = {}
    statement = select(User)
    results = session.exec(statement)
    users = results.all()
    users_dict.update({"users": users, f"{role}": role, "username": username})

    return templates.TemplateResponse("admin-area.html", {"request": request, **users_dict})


@router.get("/delete-user/{user_id}")
def delete_user(request: Request,
                     user_id: int, 
                     token_decoded_data: dict = Depends(authorise_access),
                     session: Session = Depends(get_session)):

    token_user_id = token_decoded_data['id']

    statement = select(User).where(User.id == token_user_id)
    user = session.exec(statement).first()

    role = user.role
    username = user.role

    if role not in ['admin', 'owner']:
        raise HTTPException(status_code=403, detail="Forbidden")
    
    user_for_deletion = session.get(User, user_id)
    
    if not user_for_deletion:
        raise HTTPException(status_code=404, detail="User for deletion not found")
    
    session.delete(user_for_deletion)
    session.commit()


    users_dict = {}
    statement = select(User)
    results = session.exec(statement)
    users = results.all()
    users_dict.update({"users": users, f"{role}": role, "username": username})

    return templates.TemplateResponse("admin-area.html", {"request": request, **users_dict})