from fastapi import FastAPI

app = FastAPI(
    title="Structural Engineering Analyzer API",
    description="API for preliminary structural engineering calculations.",
    version="1.0.0"
)


@app.get("/")
def read_root():
    return {
        "message": "Structural Engineering Analyzer API is running",
        "status": "success"
    }


@app.get("/health")
def health_check():
    return {
        "status": "healthy"
    }
