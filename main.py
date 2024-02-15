from fastapi import FastAPI
from fastapi.responses import FileResponse
import uvicorn 

app = FastAPI()
model_file_path = "model.txt"

@app.get("/")
async def read_root():
    return {"message": "Staging is alive"}

@app.get("/download/model")
async def download_model():
    return FileResponse(path=model_file_path, filename=model_file_path, media_type="text/plain") 

@app.get("/download/code")
async def download_code():
    pass 

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000)