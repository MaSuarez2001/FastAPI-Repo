import requests
from fastapi import FastAPI, HTTPException
from typing import Optional
from pydantic import BaseModel

# Token de GitHub 
GITHUB_API_URL = "https://api.github.com"

app = FastAPI()

#  repositorio
class Repositorio(BaseModel):
    id: Optional[int] = None
    nombre: str
    descripcion: Optional[str] = None
    url: Optional[str] = None

# (GET)
@app.get("/repos/{username}", response_model=list[Repositorio])
def get_repos(username: str):
    headers = {"Authorization": f"token {TOKEN}"}
    response = requests.get(f"{GITHUB_API_URL}/users/{username}/repos", headers=headers)

    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code, detail="Error al obtener repositorios")

    repos_data = response.json()
    return [Repositorio(id=repo["id"], nombre=repo["name"], descripcion=repo.get("description"), url=repo["html_url"]) for repo in repos_data]

# (POST)
@app.post("/repos/")
def create_repo(repo: Repositorio):
    headers = {"Authorization": f"token {TOKEN}"}
    data = {"name": repo.nombre, "description": repo.descripcion}
    response = requests.post(f"{GITHUB_API_URL}/user/repos", headers=headers, json=data)

    if response.status_code != 201:
        raise HTTPException(status_code=response.status_code, detail="Error al crear repositorio")

    return response.json()

# (PUT)
@app.put("/repos/{repo_name}")
def update_repo(repo_name: str, repo: Repositorio):
    headers = {"Authorization": f"token {TOKEN}"}
    data = {"name": repo.nombre, "description": repo.descripcion}
    response = requests.patch(f"{GITHUB_API_URL}/repos/MaSuarez2001/{repo_name}", headers=headers, json=data)

    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code, detail="Error al actualizar repositorio")

    return response.json()

# (DELETE)
@app.delete("/repos/{repo_name}")
def delete_repo(repo_name: str):
    headers = {"Authorization": f"token {TOKEN}"}
    response = requests.delete(f"{GITHUB_API_URL}/repos/MaSuarez2001/{repo_name}", headers=headers)

    if response.status_code != 204:
        raise HTTPException(status_code=response.status_code, detail="Error al eliminar repositorio")

    return {"message": "Repositorio eliminado con éxito"}