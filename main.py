from fastapi import FastAPI, UploadFile, File, Request
from fastapi.responses import JSONResponse, HTMLResponse, FileResponse
from fastapi.templating import Jinja2Templates
import uvicorn 
import pandas as pd 
from sklearn import preprocessing
from joblib import load 
import io 
import os
import shutil

from versioning import database

app = FastAPI()
templates = Jinja2Templates(directory="htmlDir")

def exec_inference(modelFile, testFile):
    data_test = pd.read_csv(testFile)
    y_test = data_test['# Letter'].values
    X_test = data_test.drop(data_test.loc[:, 'Line':'# Letter'].columns, axis = 1)
    # Data normalization (0,1)
    X_test = preprocessing.normalize(X_test, norm='l2')
    # load and Run model
    clf_lda = load(modelFile)

    score = int(clf_lda.score(X_test, y_test)*100)
    return score

def find_data_path(directory_name: str) -> str:
    data_versioning_dir = "./data_versioning/" 

    if not os.path.isdir(data_versioning_dir):
        raise FileNotFoundError("O diretório data_versioning não foi encontrado.")

    for root, dirs, files in os.walk(data_versioning_dir):
        if directory_name in dirs:
            return os.path.join(root, directory_name)

    return None

def find_model_path(directory_name: str) -> str:
    data_versioning_dir = "./model_versioning/"

    if not os.path.isdir(data_versioning_dir):
        raise FileNotFoundError("O diretório data_versioning não foi encontrado.")

    for root, dirs, files in os.walk(data_versioning_dir):
        if directory_name in dirs:
            return os.path.join(root, directory_name)

    return None

@app.get("/")
async def read_root():
    return {"message": "I'm Alive!"}

@app.post("/inference")
async def run_inference(testFile: UploadFile = File(...)):
    try:
        testContent = await testFile.read()
        score = exec_inference(modelFile="my-model/clf_lda.joblib", testFile=io.BytesIO(testContent))
        return JSONResponse(content={"message": f"Result: {score}%"}, status_code=200) 
    except Exception as e:
        return JSONResponse(content={"error": "Internal Server Error", "error": str(e)}, status_code=500)
    
@app.get("/query/dataVersioning", response_class=HTMLResponse)
async def query_data_versioning(request: Request):
    try:
        query = database.get_data_table()
        data = query.to_dict(orient='records') 
        return templates.TemplateResponse('dataVersioning.html', {'request': request, 'data': data})
    except Exception as e:
        return JSONResponse(content={"error": "Internal Server Error", "error": str(e)}, status_code=500)
    
@app.get("/query/modelVersioning", response_class=HTMLResponse)
async def query_model_versioning(request: Request):
    try:
        query = database.get_model_table()
        data = query.to_dict(orient='records')
        return templates.TemplateResponse('modelVersioning.html', {'request': request, 'data': data})
    except Exception as e:
        return JSONResponse(content={"error": "Internal Server Error", "error": str(e)}, status_code=500)
    
@app.get("/download/data/{directory_name}/")
async def download_data_directory(directory_name: str):
    directory_path = find_data_path(directory_name)
    if directory_path:
        zip_file = f"./data_versioning/{directory_name}.zip"
        shutil.make_archive(directory_path, 'zip', directory_path)
        return FileResponse(zip_file, media_type='application/zip', filename=f"{directory_name}.zip")
    else:
        return {"error": "Diretório não encontrado"}
    
@app.get("/download/model/{directory_name}/")
async def download_data_directory(directory_name: str):
    directory_path = find_model_path(directory_name)
    if directory_path:
        zip_file = f"./model_versioning/{directory_name}.zip"
        shutil.make_archive(directory_path, 'zip', directory_path)
        return FileResponse(zip_file, media_type='application/zip', filename=f"{directory_name}.zip")
    else:
        return {"error": "Diretório não encontrado"}
    
if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8001)
