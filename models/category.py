from typing import List

from pydantic import BaseModel, Field


class SubCategory(BaseModel):
    name: str = Field("")


class Category(BaseModel):
    name: str = Field("")
    subcategories: List[SubCategory] = []
