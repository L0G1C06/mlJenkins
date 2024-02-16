from fastapi import FastAPI, UploadFile, File
from fastapi.responses import StreamingResponse, JSONResponse
import os 
import uvicorn 

app = FastAPI()
model_file_path = "./staging_models/clf_lda.joblib"
staging_model_folder = "./staging_models/"

@app.get("/")
async def read_root():
    return {"message": "Staging is alive"}

@app.get("/download/model")
async def download_model():
    try:
        with open(model_file_path, "rb") as file:
            content = file.read()
    except FileNotFoundError:
        return {"error": "File not found"}
    
    headers = {
        "Content-Disposition": f"attachment; filename={model_file_path}"
    }
    return StreamingResponse(iter([content]), status_code=200, headers=headers, media_type="application/octet-stream")

@app.post("/upload/model")
async def upload_model(modelFile: UploadFile = File(...)):
    try:
        os.makedirs(staging_model_folder, exist_ok=True)

        file_path = os.path.join(staging_model_folder, modelFile.filename)
        with open(file_path, "wb") as buffer:
            buffer.write(await modelFile.read())
        
        return JSONResponse(content={"message": "File uploaded successfully", "file_name": modelFile.filename}, status_code=200)
    except Exception as e:
        return JSONResponse(content={"error": "Internal Server Error", "error": str(e)}, status_code=500)

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000)