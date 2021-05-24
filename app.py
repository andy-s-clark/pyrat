#!/usr/bin/env python3
from fastapi import Security, Depends, FastAPI, HTTPException
from fastapi.security.api_key import APIKeyQuery, APIKey
import uvicorn
from starlette.status import HTTP_403_FORBIDDEN

from config import Config
from github_compare import GithubCompare


app = FastAPI()
config = Config({
    "api_key": None,
    "github_access_token": None
})
api_key_query = APIKeyQuery(name="api_key", auto_error=False)
github_compare = GithubCompare(config.github_access_token)


async def get_api_key(api_key: str = Security(api_key_query)):
    if api_key == config.api_key:
        return api_key
    else:
        raise HTTPException(
            status_code=HTTP_403_FORBIDDEN, detail="Invalid credentials"
        )


@app.get("/healthz")
async def health(api_key: APIKey = Depends(get_api_key)):
    return {"status": "OK", "APIKey": api_key}


@app.get("/{owner}/{repo}/{base}/{head}/compare")
async def compare_commit_messages(owner: str, repo: str, base: str, head: str):
    # LATER Use an executor for the ghapi call
    return github_compare.get_commit_messages(owner, repo, base, head)


if __name__ == "__main__":
    uvicorn.run("app:app", port=8000, reload=True, debug=True, workers=1)
