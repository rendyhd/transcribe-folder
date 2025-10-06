from pydantic import BaseModel

class FolderBase(BaseModel):
    path: str

class FolderCreate(FolderBase):
    pass

class FolderUpdate(BaseModel):
    monitoring_enabled: bool

class Folder(FolderBase):
    id: int
    monitoring_enabled: bool

    class Config:
        from_attributes = True