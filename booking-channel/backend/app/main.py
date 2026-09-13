from fastapi import FastAPI

app = FastAPI(title="Booking Channel Service")

@app.get("/health")
def health_check():
    return {"status": "ok"}
