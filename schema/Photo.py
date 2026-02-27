from pydantic import BaseModel

class Photo(BaseModel):
    title: str 
    url: str