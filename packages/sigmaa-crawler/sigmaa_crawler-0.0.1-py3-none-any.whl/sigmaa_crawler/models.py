from pydantic import BaseModel

class User(BaseModel):
    matricula: int
    contraseña: str