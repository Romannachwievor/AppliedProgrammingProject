from fastapi import Body, FastAPI

app = FastAPI()

@app.get("/")
def root():
    return {"message": "Hello World"} 

@app.get("/name/{name}")
def greet_name(name: str):
    return {"message": f"Hello {name}!"}


@app.post("/process-value")
def process_input(value: float = Body(..., embed=True)):
    return {
        "original_value": value,
        "processed_value": value * 2,
    }