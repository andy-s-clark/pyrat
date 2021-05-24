#!/usr/bin/env python3
from fastapi import FastAPI
import uvicorn
from config import Config
from github_compare import GithubCompare


app = FastAPI()
config = Config()
github_compare = GithubCompare(config.github_access_token)


@app.get("/healthz")
def health():
    return {"status": "OK"}


@app.get("/{owner}/{repo}/{base}/{head}/compare")
def compare_commit_messages(owner: str, repo: str, base: str, head: str):
    return github_compare.get_commit_messages(owner, repo, base, head)


if __name__ == "__main__":
    uvicorn.run("app:app", port=8000, reload=True, debug=True, workers=1)
