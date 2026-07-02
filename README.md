#create project

uv init fastapi-uv-app

#Add FastAPI and Uvicorn

uv add fastapi uvicorn
 
 #open main.py

from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def read_root():
    return {"Hello": "World"}


#Run the server

uv run uvicorn main:app --reload
 or
uv run python main.py

#open http://localhost:8000/ in browser
