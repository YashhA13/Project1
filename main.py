from fastapi import FastAPI
from pydantic import BaseModel
from db import users_collection
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # allow frontend
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class register(BaseModel):
    email:str
    password:str


class Login(BaseModel):
    email:str
    password:str

@app.post("/auth/register")
async def registerUser(user: register):
    existing_user = users_collection.find_one({"email":user.email})

    if existing_user:
        return{
            "success":False,
            "message": "User is already registered"
        }
    users_collection.insert_one({
        "email":user.email,
        "password":user.password
    })

    return{
        "success": True,
        "message":"User registered successfully"
    }

@app.post("/auth/login")
async def loginUser(user: Login):
    db_user = users_collection.find_one({"email":user.email})

    if not db_user:
        return{
            "success":False,
            "message":"No login credentials found"
        }
    if db_user["password"] != user.password:
        return{
            "successs":False,
            "message": "Incorrect Password,Try again"
        }
    return{
        "success": True,
        "message":"Login successful"
    }