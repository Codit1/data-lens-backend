from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from App.Api import upload, search, columns

app = FastAPI()

@app.get("/")
async def root():
    return { "message": "Hello wellcome to Data lens" }


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(upload.router)
app.include_router(search.router)
app.include_router(columns.router)

