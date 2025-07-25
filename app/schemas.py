from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class ProjectCreate(BaseModel):
    title: str
    description: Optional[str] = None
    priority: int  # Deve ser um número entre 1 e 3
    status: str  # Deve ser um dos seguintes: "Planejado", "Em Andamento", "Concluído", "Cancelado"

class ProjectUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    priority: Optional[int] = None  # Deve ser um número entre 1 e 3
    status: Optional[str] = None  # Deve ser um dos seguintes: "Planejado", "Em Andamento", "Concluído", "Cancelado"

class ProjectResponse(BaseModel):
    id: str
    title: str
    description: Optional[str] = None
    priority: int  # Deve ser um número entre 1 e 3
    status: str  # Deve ser um dos seguintes: "Planejado", "Em Andamento", "Concluído", "Cancelado"
    created_at: datetime

    class Config:
        orm_mode = True