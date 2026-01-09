from fastapi import FastAPI
from data import projects, skills, data, photographs
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title="Portfolio API Gateway",
    description="Vercel + FastAPI API Gateway for Portfolio",
    version="1.0.0",
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],     # GET, POST, etc.
    allow_headers=["*"],     # allow all headers
)

@app.get("/api/data")
def get_sample_data():
    return {
        "data": [
            {"id": 1, "name": "Sample Item 1", "value": 100},
            {"id": 2, "name": "Sample Item 2", "value": 200},
            {"id": 3, "name": "Sample Item 3", "value": 300}
        ],
        "total": 3,
        "timestamp": "2024-01-01T00:00:00Z"
    }


@app.get("/api/items/{item_id}")
def get_item(item_id: int):
    return {
        "item": {
            "id": item_id,
            "name": "Sample Item " + str(item_id),
            "value": item_id * 100
        },
        "timestamp": "2024-01-01T00:00:00Z"
    }

@app.get("/api/projects")
def get_projects():
    return projects

@app.get("/api/skills")
def get_skills():
    return skills

@app.get("/api/photographs")
def get_photographs():
    return photographs

@app.get("/")
def read_root():
    return "API gatway for Vercel + FastAPI"