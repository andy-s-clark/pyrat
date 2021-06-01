import re
from typing import Set, Dict, Optional

from ghapi.core import GhApi


class GithubCompare:
    def __init__(self, github_access_token: Optional[str] = None):
        self._api = GhApi(token=github_access_token)

    def _get_commit_messages(self, owner: str, repo: str, base: str, head: str) -> Dict[str, str]:
        comparison = self._api.repos.compare_commits(owner, repo, base, head, 1, 1)
        commit_messages: Dict[str, str] = {}
        for commit in comparison.commits:
            commit_messages[commit.sha] = commit.commit.message
        return commit_messages

    def get_commit_messages_issues(self, owner: str, repo: str, base: str, head: str) -> Set[str]:
        reo = re.compile("([a-zA-Z]+-[0-9]+)")
        issue_ids: Set[str] = set()
        for _, message in self._get_commit_messages(owner, repo, base, head).items():
            m = reo.match(message)
            if m is not None:
                issue_ids.add(m.group(1))
        return issue_ids
