# Pyrat

`PYthon Release Auto-Transitioner`

## Set up local development environment

1. Install Python 3.8 and virtualenv
2. Change to the directory of your local clone of this repository

        cd ~/work/pyrat
3. Create python virtual environment

        python3 -m venv venv
4. Activate python virtual environment

        source env/bin/activate
5. Install required packages

        pip install -r requirements.txt

## Run locally

    source env/bin/activate
    export API_KEY=SOME_SECRET_TEXT_HERE
    export GITHUB_ACCESS_TOKEN=YOUR_PAT_HERE
    export JIRA_API_TOKEN=YOUR_JIRA_API_TOKEN
    export JIRA_URL=https://jira.atlassian.com
    export JIRA_USERNAME=YOUR_JIRA_USERNAME
    python app.py

## Docker

    docker build -t pyrat .
    docker run -it --name pyrat --rm -p 8000:8000 \
      -e API_KEY=SOME_SECRET_TEXT_HERE \
      -e GITHUB_ACCESS_TOKEN=YOUR_PAT_HERE \
      -e JIRA_API_TOKEN=YOUR_JIRA_API_TOKEN \
      -e JIRA_URL=https://jira.atlassian.com \
      -e JIRA_USERNAME=YOUR_JIRA_USERNAME \
      pyrat

## Usage

### Authentication

The `api_key` cookie, header, and/or query arguments provide minimal authentication.

### Health
The health check does not require authentication.

http://localhost:8000/healthz

### Swagger Docs

http://localhost:8000/docs?api_key=SOME_SECRET_TEXT_HERE

### List Jira issues from commit messages between two commits or tags

`owner`/`repo`/`base`/`head`/compare

ex. http://localhost:8000/andy-s-clark/pyrat/fd15f34/main/compare?api_key=SOME_SECRET_TEXT_HERE

### Transition issues using commit messages between two commits or tags

`owner`/`repo`/`base`/`head`/transition/`new_state`

ex. http://localhost:8000/andy-s-clark/pyrat/fd15f34c034c31a744e83813146baf3cf467e3ca/main/transition/to%20do?api_key=SOME_SECRET_TEXT_HERE
