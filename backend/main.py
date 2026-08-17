From fastapi import FastAPI

app = FastAPI(
    title="Structural Engineering Analyzer",
    description="API for structural engineering calculations",
    version="1.0.0"
)


@app.get("/")
def read_root():
    return {
        "message": "Structural Engineering Analyzer API is running"
    }
}
