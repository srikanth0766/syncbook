from fastapi import FastAPI

app = FastAPI(title="Syncbook CRS Service")

@app.get("/health")
def health_check():
    return {"status": "ok"}
