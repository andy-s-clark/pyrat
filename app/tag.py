from github import Github


class Tag:
    def __init__(self, github_api_token: str, name: str):
        self._github = Github(github_api_token)
        self._name = name

    def display(self):
        for repo in self._github.get_user().get_repos():
            print(repo.name)
        return {"name": self._name}
