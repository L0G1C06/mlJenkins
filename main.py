from fastapi import FastAPI, UploadFile, File, Request
from fastapi.responses import JSONResponse, HTMLResponse
from fastapi.templating import Jinja2Templates
import uvicorn 
import pandas as pd 
from sklearn import preprocessing
from joblib import load 
import io 

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
    
@app.get("/query/dataVersioning")
async def query_data_versioning(request: Request):
    try:
        query = database.get_data_table()
        return templates.TemplateResponse('dataVersioning.html', {'request': request, 'data': query.to_html()})
        #return JSONResponse(content={"message": f"{query}"}, status_code=200)
    except Exception as e:
        return JSONResponse(content={"error": "Internal Server Error", "error": str(e)}, status_code=500)
    
@app.get("/query/modelVersioning")
async def query_model_versioning(request: Request):
    try:
        query = database.get_model_table()
        return templates.TemplateResponse('modelVersioning.html', {'request': request, 'data': query.to_html()})
    except Exception as e:
        return JSONResponse(content={"error": "Internal Server Error", "error": str(e)}, status_code=500)
    
if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8001)
