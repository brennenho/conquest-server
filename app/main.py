from fastapi import FastAPI

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}


from app.alerts.manager import AlertManager

manager = AlertManager()
manager.check_sections()
