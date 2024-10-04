from fastapi import FastAPI

app = FastAPI()

@app.get('/')
def get_main(sort: str | None):
    pass
    return sort