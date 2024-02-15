from fastapi import FastAPI
import uvicorn 

app = FastAPI()

@app.get("/")
async def read_root():
    return {"message": "Staging is alive"}

@app.get("/download/model")
async def download_model():
    pass 

@app.get("/download/code")
async def download_code():
    pass 

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000)