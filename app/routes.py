from fastapi import APIRouter, HTTPException, Query
from typing import List, Optional
from uuid import UUID, uuid4
from datetime import datetime
from .schemas import ProjectCreate, ProjectResponse, ProjectUpdate

router = APIRouter()

# Simulação de banco de dados em memória
projects_db = {}

@router.post("/projects", response_model=ProjectResponse, status_code=201)
def create_project(project: ProjectCreate):
    project_id = str(uuid4())
    new_project = {
        "id": project_id,
        "created_at": datetime.utcnow(),
        **project.dict()
    }
    projects_db[project_id] = new_project
    return new_project

@router.get("/projects", response_model=List[ProjectResponse])
def list_projects(skip: int = Query(0, ge=0), limit: int = Query(10, gt=0), 
                  status: Optional[str] = Query(None), priority: Optional[int] = Query(None)):
    projects = list(projects_db.values())
    
    if status:
        projects = [proj for proj in projects if proj["status"] == status]
    if priority:
        projects = [proj for proj in projects if proj["priority"] == priority]
    
    return projects[skip: skip + limit]

@router.get("/projects/{project_id}", response_model=ProjectResponse)
def get_project(project_id: str):
    project = projects_db.get(project_id)
    if not project:
        raise HTTPException(status_code=404, detail="Projeto não encontrado")
    return project

@router.put("/projects/{project_id}", response_model=ProjectResponse)
def update_project(project_id: str, project: ProjectUpdate):
    stored_project = projects_db.get(project_id)
    if not stored_project:
        raise HTTPException(status_code=404, detail="Projeto não encontrado")
    
    updated_project = {**stored_project, **project.dict()}
    projects_db[project_id] = updated_project
    return updated_project

@router.delete("/projects/{project_id}", status_code=204)
def delete_project(project_id: str):
    if project_id in projects_db:
        del projects_db[project_id]
    else:
        raise HTTPException(status_code=404, detail="Projeto não encontrado")