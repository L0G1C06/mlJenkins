from fastapi import FastAPI
from fastapi.responses import StreamingResponse
import uvicorn 

app = FastAPI()
model_file_path = "./staging_models/clf_lda.joblib"

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

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000)