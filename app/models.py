from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class ProjectBase(BaseModel):
    title: str
    description: Optional[str] = None
    priority: int  # Deve ser um número entre 1 e 3
    status: str  # Deve ser um dos seguintes: "Planejado", "Em Andamento", "Concluído", "Cancelado"

class ProjectCreate(ProjectBase):
    pass

class ProjectUpdate(ProjectBase):
    pass

class ProjectResponse(ProjectBase):
    id: str
    created_at: datetime

    class Config:
        orm_mode = True