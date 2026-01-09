from fastapi import FastAPI
from data import projects, skills, data, photographs
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

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
def get_data():
    return JSONResponse(data)

@app.get("/api/projects")
def get_projects():
    return JSONResponse(projects)

@app.get("/api/skills")
def get_skills():
    return JSONResponse(skills)

@app.get("/api/photographs")
def get_photographs():
    return JSONResponse(photographs)

@app.get("/")
def read_root():
    return JSONResponse({"message": "API gateway for Vercel + FastAPI"})