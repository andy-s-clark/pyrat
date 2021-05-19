from configuration import Configuration
from fastapi import FastAPI
from tag import Tag

app = FastAPI()
config = Configuration()


@app.get("/healthz")
def read_health():
    return {"status": "OK"}


@app.get("/tag/{tag_id}")
def read_item(tag_id: str):
    tag = Tag(config.read_item("github_api_token"), tag_id)
    return tag.display()
