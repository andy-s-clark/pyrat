#!/usr/bin/env python3
from fastapi import Security, Depends, FastAPI, HTTPException
from fastapi.openapi.docs import get_swagger_ui_html
from fastapi.openapi.utils import get_openapi
from fastapi.security.api_key import APIKey, APIKeyCookie, APIKeyHeader, APIKeyQuery
from fastcore.utils import HTTP404NotFoundError
import logging
from jira import JIRA, exceptions
from typing import Dict
from starlette.status import HTTP_403_FORBIDDEN, HTTP_404_NOT_FOUND
from starlette.responses import JSONResponse
import uvicorn

from config import Config
from github_compare import GithubCompare

app = FastAPI(docs_url=None, redoc_url=None, openapi_url=None)
logger = logging.getLogger()
config = Config({
    "api_key": None,
    "github_access_token": None,
    "jira_api_token": None,
    "jira_url": "https://jira.atlassian.com",
    "jira_username": None
})
api_key_cookie = APIKeyCookie(name="api_key", auto_error=False)
api_key_header = APIKeyHeader(name="api_key", auto_error=False)
api_key_query = APIKeyQuery(name="api_key", auto_error=False)
github_compare = GithubCompare(config.github_access_token)
jira = JIRA(basic_auth=(config.jira_username, config.jira_api_token), server=config.jira_url)


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
    try:
        return github_compare.get_commit_messages_issues(owner, repo, base, head)
    except HTTP404NotFoundError as ex:
        raise HTTPException(
            status_code=HTTP_404_NOT_FOUND, detail="{} {}".format(ex.url, ex.reason)
        )


# Allow using a GET for client simplicity
@app.put("/{owner}/{repo}/{base}/{head}/transition/{new_state}")
@app.get("/{owner}/{repo}/{base}/{head}/transition/{new_state}")
def transition_by_commit_comparison(owner: str, repo: str, base: str, head: str, new_state: str,
                                    _: APIKey = Depends(get_api_key)) -> Dict[str, bool]:
    attempted_issues: Dict[str, bool] = {}
    # LATER Use async and executors for the ghapi and Jira calls
    for issue_id in github_compare.get_commit_messages_issues(owner, repo, base, head):
        attempted_issues[issue_id] = False
        try:
            logger.info("Attempting to transition {} to {}".format(issue_id, new_state))
            issue = jira.issue(issue_id)
            for transition in jira.transitions(issue):
                if transition["name"].lower() == new_state.lower():
                    jira.transition_issue(issue, transition["id"])
                    attempted_issues[issue_id] = True
                    break
        except exceptions.JIRAError as ex:
            logger.warning(ex)
    return attempted_issues


@app.get("/issue/{issue_id}/status")
async def get_issue_status(issue_id: str, _: APIKey = Depends(get_api_key)) -> str:
    return str(jira.issue(issue_id).fields.status)


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
