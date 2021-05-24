import typing

from ghapi.core import GhApi


class GithubCompare:
    def __init__(self, github_access_token: typing.Optional[str] = None):
        self._api = GhApi(token=github_access_token)

    def get_commit_messages(self, owner: str, repo: str, base: str, head: str):
        comparison = self._api.repos.compare_commits(owner, repo, base, head, 1, 1)
        commit_messages = {}
        for commit in comparison.commits:
            commit_messages[commit.sha] = commit.commit.message
        return commit_messages
