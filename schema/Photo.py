from pydantic import BaseModel, Field
from typing import Optional

class Photo(BaseModel):
    id: Optional[int] = Field(description="primary key generated db side")  
    filename: str = Field(...,description="filename")
    url: str = Field(..., description="Cloudinary URL of the image")  
    width: int = Field(default=1080, description="Image width in pixels") 
    height: int = Field(default=1920, description="Image height in pixels") 
    category: Optional[str] = Field(
        default="nature",
        description="Photo category",
        examples=["landscape", "nature"]
    )
