import os
import random
import json
from turtle import title
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi import FastAPI, HTTPException, Query
from enum import Enum

from model.db import Session, Property, engine

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")


@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    ''' renders the main page '''
    return templates.TemplateResponse("main.html", {"request": request, "id": 1})


@app.get("/environment")
async def environment():
    return {
        "ENVIRONMENT": os.environ.get("ENVIRONMENT"),
        "DB_HOST": os.environ.get("DB_HOST"),
        "DB_USER": os.environ.get("DB_USER"),
        "DB_PASSWORD": os.environ.get("DB_PASSWORD"),
        "DB_PORT": os.environ.get("DB_PORT"),
        "DB_NAME": os.environ.get("DB_NAME"),
    }


@app.post("/add_record")
async def add_record( title:str,  price:float , area:float, type: str=Query("buy", enum=["buy", "rent"]), id:int = None) -> json : 
    ''' Adds or updates the record based on the ID'''
    
    with Session() as session:
        query = session.query(Property).filter(Property.id==id).first()
        if not query: query = Property()
        query.title = title
        query.type = price
        query.area = area
        
        session.add(query)
        session.commit()
        return {'status': 'ok', 'msg': 'record added'}


@app.get("/get_data")
async def get_data( 
                   type:str=None, 
                   from_price:float=None , 
                   to_price:float=None, 
                   from_area:float=None, 
                   to_area:float=None, 
                   ) -> json : 
    
    ''' get the date for the map   '''
    print('get_data')
    
    print('from_price: ', from_price)
    print('to_price: ', to_price)
    print('from_area: ', from_area)
    print('to_area: ', to_area)
    
    result = {}
    with Session() as session:
        query = session.query(Property).order_by(Property.id)
        
        if from_price:
            query = query.filter(Property.price >= from_price)
        if to_price:
            query = query.filter(Property.price <= to_price)    
        if from_area:
            query = query.filter(Property.area >= from_area)
        if to_area:
            query = query.filter(Property.area <= to_area)
            
        for i in query.all():
            result[str(i.id)] = i.as_dict()
        return result

@app.get("/get_random_data")
async def get_random_data():
    data = {}
    to = random.randint(0, 100)
    for i in range(0, 100):
        data[f"{i}"] = {
            "title": "Example 2",
            "lon": 14.4378 + random.uniform(-0.5, 0.5),
            "lat": 50.0755 + random.uniform(-0.3, 0.3),
            "img_src": f"/static/imgs/random/{random.randint(1,3)}.png",
            "url": "https://mobiletechtracker.co.uk/",
            "price": random.uniform(0, 20000000),
            "currency": "EUR",
            "area": random.uniform(0, 20000000),
            "measurement": "sqft",
        }
    return data
