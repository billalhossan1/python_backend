from fastapi import datastructures
import uvicorn

from app.factory import create_app
from app.core.config import settings
from app.equipment.models import Equipment

app = create_app()
print(f"Equipment doc: {Equipment.__doc__}")

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host=settings.host,
        port=settings.port,
        reload=settings.debug,
    )




for n in range(5 , 10):
    print(f" itertae ${n}")
