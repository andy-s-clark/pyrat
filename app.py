#!/usr/bin/env python3
from fastapi import Security, Depends, FastAPI, HTTPException
from fastapi.openapi.docs import get_swagger_ui_html
from fastapi.openapi.utils import get_openapi
from fastapi.security.api_key import APIKey, APIKeyCookie, APIKeyHeader, APIKeyQuery
import uvicorn
from starlette.status import HTTP_403_FORBIDDEN
from starlette.responses import JSONResponse

from config import Config
from github_compare import GithubCompare


app = FastAPI(docs_url=None, redoc_url=None, openapi_url=None)
config = Config({
    "api_key": None,
    "github_access_token": None
})
api_key_cookie = APIKeyCookie(name="api_key", auto_error=False)
api_key_header = APIKeyHeader(name="api_key", auto_error=False)
api_key_query = APIKeyQuery(name="api_key", auto_error=False)
github_compare = GithubCompare(config.github_access_token)


async def get_api_key(
        cookie_api_key: str = Security(api_key_cookie),
        header_api_key: str = Security(api_key_header),
        query_api_key: str = Security(api_key_query)
):
    if cookie_api_key == config.api_key:
        return cookie_api_key
    elif header_api_key == config.api_key:
        return header_api_key
    elif query_api_key == config.api_key:
        return query_api_key
    else:
        raise HTTPException(
            status_code=HTTP_403_FORBIDDEN, detail="Invalid credentials"
        )


@app.get("/healthz")
async def get_health():
    return {"status": "OK"}


@app.get("/{owner}/{repo}/{base}/{head}/compare")
async def get_compare_commit_messages(owner: str, repo: str, base: str, head: str,
                                      _: APIKey = Depends(get_api_key)):
    # LATER Use an executor for the ghapi call
    return github_compare.get_commit_messages(owner, repo, base, head)


@app.get("/openapi.json", tags=["documentation"])
async def get_open_api_endpoint(_: APIKey = Depends(get_api_key)):
    return JSONResponse(get_openapi(title="Pyrat", version="1", routes=app.routes))


@app.get("/docs")
async def get_docs(_: APIKey = Depends(get_api_key)):
    response = get_swagger_ui_html(openapi_url="/openapi.json", title="docs")
    response.set_cookie(
        "api_key",
        value=config.api_key,
        httponly=True
    )
    return response


if __name__ == "__main__":
    uvicorn.run("app:app", port=8000, reload=True, debug=True, workers=1)
