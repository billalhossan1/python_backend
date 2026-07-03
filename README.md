#create project

```bash
uv init fastapi-uv-app
```

# Add FastAPI and Uvicorn
```bash
uv add fastapi uvicorn
```


# postgree sql

```bash
uv add sqlalchemy asyncpg aiosqlite greenlet```
 
# open main.py

```from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def read_root():
    return {"Hello": "World"}

```
# Run the server

```bash
uv run uvicorn main:app --reload
 or
uv run python main.py
```
#open http://localhost:8000/ in browser


DATABASE
install docker

brew install --cask docker


create db

docker run --name my-postgres -p 5432:5432 -e POSTGRES_USER=postgres -e POSTGRES_PASSWORD=postgres -e POSTGRES_DB=fastapi_db -d postgres
