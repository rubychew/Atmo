from fastapi import APIRouter, Request, HTTPException, Depends
from fastapi.templating import Jinja2Templates
from jose import jwt, JWTError, ExpiredSignatureError
import os
from dotenv import load_dotenv
from atmo_db.models import User, Audio_File
from atmo_db.database import get_session
from sqlmodel import Session, select

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
@router.get("/audio-files/{user_id}")
async def list_files(request: Request,
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

    # object to be populated and passed to front end through jinja template
    user_data = {}
    role = user.role
    username = user.username
    user_data.update({f"{role}": role, "username": username})

    statement = select(Audio_File).where(token_user_id == Audio_File.user_id).limit(10)
    results = session.exec(statement)
    audio_files = results.all()

    user_data.update({"audio_files": audio_files})

    print(user_data)
    
    return templates.TemplateResponse("audio-files.html", {"request": request, **user_data})


