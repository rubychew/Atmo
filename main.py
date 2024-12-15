from fastapi import FastAPI
from atmo_db.database import engine
from sqlmodel import SQLModel
# Model imports required for the engine to create the schema
from atmo_db.models import User, Audio_File
from starlette.middleware.base import BaseHTTPMiddleware

from routers import auth, audio_files, admin

app = FastAPI()

#create db schema on startup
@app.on_event("startup")
async def startup_event():
    SQLModel.metadata.create_all(engine)
app.include_router(auth.router)
app.include_router(audio_files.router)
app.include_router(admin.router)

# add security headers
# code from rverma253/SecureWebDevLabs 6 CSRF secure_app_with_headers.py
class SecurityHeaders(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        response = await call_next(request)
        # Content Security Policy (CSP)
        # this exception is a chatgpt fix to allow for tailwind css
        response.headers['Content-Security-Policy'] = (
            "default-src 'self'; "  # Allow resources from same origin
            "script-src 'self' https://cdn.tailwindcss.com 'unsafe-inline';"  # Allow Tailwind JS from its CDN
            "style-src 'self' https://cdn.tailwindcss.com 'unsafe-inline';"  # Allow Tailwind CSS from its CDN
            "font-src 'self' https://cdn.tailwindcss.com;"  # Allow fonts if needed
            "frame-ancestors 'none';"
        )
        # Prevent MIME type sniffing
        response.headers['X-Content-Type-Options'] = 'nosniff'
        # Clickjacking protection
        response.headers['X-Frame-Options'] = 'DENY'
        # XSS Protection Header (for older browsers)
        response.headers['X-XSS-Protection'] = '1; mode=block'
        return response
    
app.add_middleware(SecurityHeaders)