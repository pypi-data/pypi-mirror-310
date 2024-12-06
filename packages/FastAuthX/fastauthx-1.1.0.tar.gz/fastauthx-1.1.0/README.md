# FastAuthX

**FastAuthX** is a plug-and-play authentication package for FastAPI, designed to simplify and streamline the implementation of authentication with minimal setup. It supports token management, user validation, and password hashing, making it easy to integrate into your FastAPI applications.

## Features
- Simple and fast authentication for FastAPI
- Automatic JWT token management (create, verify, and refresh)
- Password hashing with `bcrypt`
- Built-in OAuth2 password flow
- Easy database integration with SQLAlchemy
- Configurable and extensible (with a few lines of code)

## Installation

To install **FastAuthX**, run the following command:

```bash
pip install FastAuthX


Usage
1. Initialize the authentication handler in your FastAPI app

from fastapi import FastAPI
from FastAuthX import AuthHandler

app = FastAPI()

# Initialize with your database URL
auth_handler = AuthHandler(DATABASE_URL="sqlite:///./database.db")


2. Use the AuthHandler to implement login and signup endpoints


from fastapi import Depends
from FastAuthX import schemas

@app.post("/login")
def login(request: schemas.Login, db: Session = Depends(get_db)):
    return auth_handler.login(request, db)

@app.post("/signup")
def signup(request: schemas.Signup, db: Session = Depends(get_db)):
    return auth_handler.signup(request, db)



3. Protect routes with authentication

from fastapi import Depends
from FastAuthX import AuthHandler, get_current_user

@app.get("/profile")
def profile(current_user: User = Depends(get_current_user)):
    return {"user": current_user}


Configuration
You can customize the authentication handler by passing the following arguments during initialization:

DATABASE_URL: Your database URL (e.g., "sqlite:///./database.db")
access_token_expire_min: Token expiration time in minutes (default: 15 minutes)
refresh_token_expire_day: Refresh token expiration time in days (default: 7 days)
ALGORITHM: JWT algorithm (default: HS256)
app_secret_key: The secret key for signing JWT tokens

Example
Here's a minimal example of a FastAPI application using FastAuthX:

from fastapi import FastAPI, Depends
from FastAuthX import AuthHandler, schemas

app = FastAPI()

# Initialize the authentication handler with your database URL
auth_handler = AuthHandler(DATABASE_URL="sqlite:///./database.db")

@app.post("/login")
def login(request: schemas.Login, db: Session = Depends(get_db)):
    return auth_handler.login(request, db)

@app.get("/profile")
def profile(current_user: User = Depends(get_current_user)):
    return {"user": current_user}


