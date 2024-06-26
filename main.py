from fastapi import FastAPI, Request, Query
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import JSONResponse
import uvicorn
import torch
import tensorflow as tf
from transformers import BertTokenizer, TFBertForSequenceClassification
import os

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")


@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    print('Request for index page received')
    return templates.TemplateResponse('index.html', {"request": request})

@app.get('/favicon.ico')
async def favicon():
    file_name = 'favicon.ico'
    file_path = './static/' + file_name
    return FileResponse(path=file_path, headers={'mimetype': 'image/vnd.microsoft.icon'})

@app.get('/hello', response_class=HTMLResponse)
async def hello(request: Request, title: str = Query(...)):
    print(f'Request for hello page received with title={title}')
    return templates.TemplateResponse('hello.html', {"request": request, 'title': title})


@app.get("/get-tags", response_class=JSONResponse)
async def get_title(title: str = Query(...)):
    tags = title.split(" ")
    return {"title": title, "tags":tags}

if __name__ == '__main__':
    uvicorn.run('main:app', host='0.0.0.0', port=8000)
