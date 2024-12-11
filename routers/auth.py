from fastapi import APIRouter, Request, Form, HTTPException, Depends
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse
from typing_extensions import Annotated
from passlib.context import CryptContext
from atmo_db.models import User
from datetime import datetime, timezone
import re
from atmo_db.database import get_session
from sqlmodel import Session, select

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
async def authenticate_login(email: Annotated[str, Form()],
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
    
    # otherwise issue JWT token and redirect to TOTP page
    return {'Success': 'logged in'}
    
