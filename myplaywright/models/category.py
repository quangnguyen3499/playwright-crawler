from pydantic import BaseModel, Field
from typing import List


class SubCategory(BaseModel):
    name: str = Field("")

class Category(BaseModel):
    name: str = Field("")
    subcategories: List[SubCategory] = []
