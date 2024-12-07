from __future__ import annotations

from pydantic import BaseModel, Field, RootModel


class PetBase(BaseModel):
    name: str
    tag: str | None = None


class PetCreate(PetBase):
    pass


class Pet(PetBase):
    id: int


class Pets(RootModel):
    root: list[Pet] = Field(..., description="list of pet")


class Error(BaseModel):
    code: int
    message: str
