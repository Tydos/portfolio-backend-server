"""Photo schema model for database and API validation."""

from pydantic import BaseModel, Field, HttpUrl, field_validator
from typing import Optional, Literal


class Photo(BaseModel):
    """Pydantic model for photograph data validation."""

    id: Optional[int] = Field(default=None, description="primary key generated db side")
    filename: str = Field(..., min_length=1, description="filename")
    url: HttpUrl = Field(..., description="Cloudinary URL of the image")
    width: int = Field(default=1080, gt=0, description="Image width in pixels")
    height: int = Field(default=1920, gt=0, description="Image height in pixels")
    category: Literal["nature", "landscape", "urban", "portrait", "abstract", "other"] = Field(
        default="nature",
        description="Photo category"
    )

    @field_validator('filename')
    @classmethod
    def validate_filename_no_traversal(cls, v: str) -> str:
        """Reject path traversal characters in filename."""
        if '..' in v or '/' in v or '\\' in v:
            raise ValueError("Filename cannot contain path traversal characters (.., /, \\)")
        return v
