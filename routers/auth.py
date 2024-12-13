from fastapi import APIRouter, Request, Response, Form, HTTPException, Depends
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse
from typing_extensions import Annotated
from passlib.context import CryptContext
from atmo_db.models import User
from datetime import datetime, timezone, timedelta
import re
from atmo_db.database import get_session
from sqlmodel import Session, select
import os
from dotenv import load_dotenv
from jose import jwt

load_dotenv()

router = APIRouter()
templates = Jinja2Templates(directory="templates")

bcrypt_context = CryptContext(schemes=['bcrypt'], deprecated='auto')

# helper method -----------------------------------------------------------------------------
def test_email_domain(email: str):
    # temporary domain restriction for application rollout
    reg = "[A-Za-z]*.*\\d*@[a-z]*.*ncirl.ie"
    compiled = re.compile(reg)
    domain_valid = re.search(compiled, email)

    if not domain_valid:
        raise HTTPException(status_code=400, detail="Bad request.")
    
# routes -------------------------------------------------------------------------------------
@router.get("/")
async def get_sign_in(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@router.get("/register")
def register(request: Request):
    return templates.TemplateResponse("register.html", {"request": request})


@router.post("/create-user", status_code=201)
async def create_standard_user(username: Annotated[str, Form()], 
                               email: Annotated[str, Form()],
                               password: Annotated[str, Form()],
                               repassword: Annotated[str, Form()], session: Session = Depends(get_session)):
    
    # temporary domain restriction for application rollout
    test_email_domain(email)
    
    if password != repassword:
        raise HTTPException(status_code=400, detail="Bad request: passwords do not match!")
    
    #check for password complexty and password length min chars max 20
    reg = "^(?=.*[a-z])(?=.*[A-Z])(?=.*\\d)(?=.*[@$!%*#?&])[A-Za-z\\d@$!#%*?&_]{8,20}$"
    compiled = re.compile(reg)
    complexity_valid = re.search(compiled, password)

    if not complexity_valid:
        raise HTTPException(status_code=400, detail="Bad request: password complexity requirements not met.")
    
    # guard against not recieving data from all required fields
    if not username and not email and not password:
        raise HTTPException(status_code=400, detail="Bad request: missing fields.")


    standard_user = User(
        username = username,
        role = "standard",
        created_at = datetime.now(timezone.utc),
        email = email,
        password = bcrypt_context.hash(password)
    )

    session.add(standard_user)
    session.commit()

    return RedirectResponse(url="/registration-success", status_code=302)

@router.get("/registration-success")
def register(request: Request):
    return templates.TemplateResponse("registration-success.html", {"request": request})


# login / authentication routes -------------------------------------------------------------------

@router.post("/login")
async def authenticate_login(response: Response, email: Annotated[str, Form()],
                                password: Annotated[str, Form()],
                                session: Session = Depends(get_session)):

    # temporary domain restriction for application rollout
    test_email_domain(email)
   
    statement = select(User).where(User.email == email)
    user = session.exec(statement).first()

    if not user:
        return 'Authentication Failed'
    
    if not bcrypt_context.verify(password, user.password):
        return 'Authentication Failed'
    
    # otherwise issue JWT token and redirect
    jwt_token = create_jwt_token(user.email, user.id, timedelta(minutes=60))

    response = RedirectResponse(url=f'/audio-files/{user.id}', status_code=303)

    #cookie config to include
    # domain
    # same site strict - requests must originate from the same-site
    # secure todo - need to set up ssl
    # http only
    # max age is effectively already set in the jwt token with the delta from login
    response.set_cookie(key='auth_token', value=jwt_token, httponly=True, samesite='Strict')
    return response


def create_jwt_token(email: str, user_id: int, delta: timedelta):

    encode = {'sub': email, 'id': user_id}

    # token will expire at given delta
    expiry_time = datetime.now(timezone.utc) + delta
    encode.update({
        'exp': expiry_time
    })

    KEY = os.getenv("SECRET")
    ALGORITHM = os.getenv("ALGORITHM")

    jwt_token = jwt.encode(encode, KEY, ALGORITHM)

    return jwt_token


# logout remove jwt cookie ----------------------------------------------------------------------
@router.get("/logout")
async def logout(request: Request, response: Response):
    response = templates.TemplateResponse("index.html", {"request": request})
    response.delete_cookie('auth_token')
    return response