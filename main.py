'''
This sample is written using python fastapi ASGI compliant package.
It connects to MongoDB using async motor package.

to run: uvicorn main:app --reload
'''
from datetime import date
from fastapi import FastAPI
from pydantic import BaseModel
from bson.objectid import ObjectId
from motor import motor_asyncio
from asyncio import sleep
from datetime import datetime

DB_HOST = 'localhost'
DB_PORT = 27017
DB_NAME = 'manoj'

client = motor_asyncio.AsyncIOMotorClient( DB_HOST, DB_PORT )
db = client[ DB_NAME ]

class Person( BaseModel ):
    name: str

app = FastAPI()

@app.get("/")
async def root():
    await sleep( 10 )
    curDT = datetime.now()
    date_time: str = curDT.strftime("%m/%d/%Y, %H:%M:%S")
    return { "message": "Hello World!: " + date_time }

@app.get("/people")
async def get_people():
    response = []
    cursor = db.manoj.find() 
    for document in await cursor.to_list( length=100 ):
        # convert _id to string
        document['_id'] = str(document['_id'])
        response.append( document )

    return response

@app.get("/people/{person_id}")
async def path_params(person_id: str):
    document = await db.manoj.find_one({"_id": ObjectId( person_id )})
    # convert _id to string
    document['_id'] = str(document['_id'])

    return document

@app.get("/query")
async def query_params(person_id: str):
    document = await db.manoj.find_one({"_id": ObjectId( person_id )})
    # convert _id to string
    document['_id'] = str(document['_id'])

    return document

@app.post("/people")
async def create_item(item: Person):
    '''
    This is used to create an item in database
    '''
    result = await db.manoj.insert_one({"name": item.name})

    return { "_id": str( result.inserted_id )}

@app.delete("/people/{person_id}")
async def path_params(person_id: str):
    result = await db.manoj.delete_one({"_id": ObjectId( person_id )})

    return { "deleted_items": result.deleted_count }
