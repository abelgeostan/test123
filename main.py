from typing import Annotated

from fastapi import Depends, FastAPI
from pydantic import BaseModel, EmailStr
from sqlmodel import Field, Session, SQLModel, create_engine, select



class User(BaseModel,SQLModel, table=True):
    username: str
    email: EmailStr
    password: str

SQLALCHEMY_DATABASE_URL = "postgresql://postgres:mysecretpassword@localhost:5432/my_fastapi_db"

# Create the SQLAlchemy engine
engine = create_engine(SQLALCHEMY_DATABASE_URL)

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)


def get_session():
    with Session(engine) as session:
        yield session

SessionDep = Annotated[Session, Depends(get_session)]

app = FastAPI()

@app.on_event("startup")
def on_startup():
    create_db_and_tables()


@app.post("/login")
async def user_login(user: User,session: SessionDep):
    session.add(user)
    session.commit()
    session.refresh(user)
    return user