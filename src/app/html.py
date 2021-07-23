from fastapi import FastAPI, Request, Form, File, UploadFile
# from fastapi.templating import Jinja2Templates
# from starlette.responses import FileResponse

# from src.utils.helpers import convertBytesToString
# from src.app.model_pred import process_data_for_model
# import pandas as pd 
# import pickle
# from io import StringIO
# import sqlite3
# from .schemas import (
#     RequestBody,
#     ResponseBody,
#     TextSample)

from typing import List

# from fastapi import Depends, FastAPI, HTTPException
# from sqlalchemy.orm import Session

# from . import schemas #crud, models, 
# from .database import SessionLocal, engine
# import databases
from databases import Database


app = FastAPI()
# templates = Jinja2Templates(directory='templates/')

# database = Database("sqlite:///./music.db")
from src.app import crud

@app.get("/get_titles_by_genre/")
async def get_titles_by_genre(genre: str):
    # query = f"SELECT title FROM titles_and_genre WHERE predictions='{str(genre)}'"
    # results = await database.fetch_all(query=query)
    results = await crud.get_titles_by_genre(genre)
    return results

@app.get("/get_genre/")
async def get_genre():
    results = await crud.get_genre()
    return results

@app.post("/predict/")
async def predict(file: UploadFile = File(...)):
    results = await crud.predict(file)
    return results

# @app.get('/form')
# def form_post(request: Request):
#     result = 'Type a number'
#     return templates.TemplateResponse('form.html', context={'request': request, 'result': result})


# @app.post('/form')
# def form_post(request: Request, num: int = Form(...)):
#     result = spell_number(num)
#     return templates.TemplateResponse('form.html', context={'request': request, 'result': result, 'num': num})

# # with open('./models/model.pkl', "rb") as rf:
# #     clf = pickle.load(rf)

# # @app.post("/predict")
# # async def predict(body: RequestBody):
# #     data = np.array(body.to_array())
# #     print('data', data)
# #     probas = clf.predict_proba(data)
# #     predictions = probas.argmax(axis=1)
# #     # predictions = process_data_for_model(data)

# #     return {
# #         "predictions": (
# #             np.tile(clf.classes_, (len(predictions), 1))[
# #                 np.arange(len(predictions)), predictions
# #             ].tolist()
# #         ),
# #         "probabilities": probas[np.arange(len(predictions)), predictions].tolist(),
# #     }

# @app.get('/checkbox')
# def form_post(request: Request):
#     result = 'Type a number'
#     return templates.TemplateResponse('checkbox.html', context={'request': request, 'result': result})


# @app.post('/checkbox')
# def form_post(request: Request, num: int = Form(...), multiply_by_2: bool = Form(False)):
#     result = spell_number(num, multiply_by_2)
#     return templates.TemplateResponse('checkbox.html', context={'request': request, 'result': result, 'num': num})


# @app.get('/download')
# def form_post(request: Request):
#     result = 'Type a number'
#     return templates.TemplateResponse('download.html', context={'request': request, 'result': result})


# @app.post('/download')
# def form_post(request: Request, num: int = Form(...), multiply_by_2: bool = Form(False), action: str = Form(...)):
#     if action == 'convert':
#         result = spell_number(num, multiply_by_2)
#         return templates.TemplateResponse('download.html', context={'request': request, 'result': result, 'num': num})
#     elif action == 'download':
#         # Requires aiofiles
#         result = spell_number(num, multiply_by_2)
#         filepath = save_to_text(result, num)
#         return FileResponse(filepath, media_type='application/octet-stream', filename='{}.txt'.format(num))
