#!/usr/bin/env python3
from flask import Flask
from config import Config
from github_compare import GithubCompare


app = Flask(__name__)
config = Config()
github_compare = GithubCompare(config.github_access_token)


@app.route("/healthz")
def health():
    return {"status": "OK"}


@app.route("/<string:owner>/<string:repo>/<string:base>/<string:head>/compare")
def compare_messages(owner: str, repo: str, base: str, head: str):
    return github_compare.get_commit_messages(owner, repo, base, head)


if __name__ == "__main__":
    app.run()
