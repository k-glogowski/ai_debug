from fastapi import FastAPI

app = FastAPI(title="Hello API")


@app.get("/")
def root():
    return {"message": "Hello World"}
