from fastapi import FastAPI
from App.Api import upload, search, columns

app = FastAPI()

@app.get("/")
async def root():
    return { "message": "Hello wellcome to Data lens" }

app.include_router(upload.router)
app.include_router(search.router)
app.include_router(columns.router)

