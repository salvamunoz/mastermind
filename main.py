from fastapi import FastAPI

app = FastAPI()


@app.get("/")
def get_root_page():
    return {"Hello": "World"}

