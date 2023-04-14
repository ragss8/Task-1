from fastapi import FastAPI
from app.user import user 
app = FastAPI()
app.include_router(user)

from fastapi import APIRouter , Body
import json
from bson import ObjectId
user = APIRouter() 
from bson import json_util



#from config.db import SampleTable
from pymongo import MongoClient
mongodb_uri ='mongodb+srv://raghugaikwad8641:Raghugaikwad8@userinfo.d4n8sns.mongodb.net/?retryWrites=true&w=majority'
port = 8000
conn = MongoClient(mongodb_uri,port)
Database = conn.get_database('userinfo')
print(Database)
SampleTable = Database.SampleTable
print(SampleTable)


#from schemas.user import serializeDict, serializeList
def userEntity(user) -> dict:
    return {
        'id':str(user["_id"]),
        'name':user["name"],
        'email':user["email"],
        'phone':user["phone"],
        'api_key':user["api_key"],
        'api_secret_key':user["api_secret_key"],
        'access_token':user["access_token"],
        'token_expiry_time':user["token_expiry_time"],
        'token_updated_at':user["token_updated_at"]
    }

def usersEntity(users) -> list:
    return [userEntity(user) for user in users]


def serializeDict(a) -> dict:
    return {**{i:str(a[i]) for i in a if i=='_id'},**{i:a[i] for i in a if i!='_id'}}

def serializeList(entity) -> list:
    return [serializeDict(a) for a in entity]


#from models.user import User
from datetime import datetime , timedelta
from pydantic import BaseModel, EmailStr
import jwt

class User(BaseModel):
    name: str 
    email: EmailStr
    phone: str 
    api_key: str 
    api_secret_key: str 
    access_token:str 
    token_expiry_time:datetime
    token_updated_at:datetime


    """To check whether the token is expired or not if the token is expired we will generate a new token"""

def is_token_expired(self) -> bool:
        return self.token_expiry_time <= datetime.now()


def generate_jwt_token(email:str):
    token_payload = {
        "sub":email,
        "exp": int((datetime.now() + timedelta(days=1)).timestamp()), 
    }
    token = jwt.encode(token_payload, "SECRET_KEY", algorithm="HS256")
    print(token)  
    return(token)
    
@user.get('/')
async def find_all_users():
   return serializeList(SampleTable.find())  

""" @user.get('/{id}')
async def find_one_user(id, user:User):
    return serializeDict(SampleTable.find_one({"_id":ObjectId(id)})) """

@user.post('/')
async def create_user(user: dict = Body(...)):
    access_token=generate_jwt_token(user["email"])
    user["access_token"]=access_token
    user["token_updated_at"] = datetime.now()
    user["token_expiry_time"] = datetime.now() + timedelta(days=1)
    print(user)
    info=SampleTable.insert_one(dict(user))
    print(info)  

@user.put('/{id}')
async def update_access_token(id):
    local=SampleTable.find_one({"_id":ObjectId(id)})
    print(local["token_expiry_time"])
    if local["token_expiry_time"] <= datetime.now():
        filter = {"_id": ObjectId(str(id))}
        newvalues = {
        "$set": {"access_token":generate_jwt_token(local["email"]), "token_updated_at": datetime.now(),"token_expiry_time":datetime.now() + timedelta(days=1)}
        }
        print(newvalues)
        """ newvalues = {
        "$set": {"access_token": local["access_token"], "token_updated_at": local["token_updated_at"]}
        } """
        SampleTable.update_one(filter, newvalues)
    return json.dumps(local,default=json_util.default)   

@user.delete('/{id}')
async def delete_user(id,user: User):
    return serializeDict(SampleTable.find_one_and_delete({"_id":ObjectId(id)}))

