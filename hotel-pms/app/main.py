from fastapi import FastAPI

app = FastAPI(title="Hotel PMS Service")

@app.get("/health")
def health_check():
    return {"status": "ok"}
