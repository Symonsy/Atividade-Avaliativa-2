from typing import Optional
from sqlmodel import Field, Session, SQLModel, create_engine, select
from fastapi import FastAPI, HTTPException

class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    email: str
    age: Optional[int] = None
    phone: Optional[str] = None

sqlite_file_name = "database.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"
engine = create_engine(sqlite_url, echo=True)

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

app = FastAPI()

@app.on_event("startup")
def on_startup():
    create_db_and_tables()

@app.get("/users/")
def read_users():
    with Session(engine) as session:
        users = session.exec(select(User)).all()
    return users

@app.get("/users/by-email/{email}")
def get_user_by_email(email: str):
    with Session(engine) as session:
        statement = select(User).where(User.email == email)
        user = session.exec(statement).first()
        if not user:
            raise HTTPException(status_code=404, detail="Usuário não encontrado.")
    return user

@app.post("/users/", status_code=201)
def create_user(user: User):
    with Session(engine) as session:
        if session.exec(select(User).where(User.email == user.email)).first():
            raise HTTPException(status_code=400, detail="Email já cadastrado.")
        session.add(user)
        session.commit()
        session.refresh(user)
    return user

from fastapi import Body
@app.put("/users/{email}")
def update_user(email: str, updated_data: dict = Body(...)):
    with Session(engine) as session:
        statement = select(User).where(User.email == email)
        user = session.exec(statement).first()
        if not user:
            raise HTTPException(status_code=404, detail="Usuário não encontrado.")
        for key, value in updated_data.items():
            setattr(user, key, value)
        session.add(user)
        session.commit()
        session.refresh(user)
    return user

@app.delete("/users/{email}")
def delete_user(email: str):
    with Session(engine) as session:
        statement = select(User).where(User.email == email)
        user = session.exec(statement).first()
        if not user:
            raise HTTPException(status_code=404, detail="Usuário não encontrado.")
        session.delete(user)
        session.commit()
    return {"detail": "Usuário removido com sucesso."}