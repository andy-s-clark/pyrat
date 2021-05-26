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
    python app.py

## Docker

    docker build -t pyrat .
    docker run -it --name pyrat --rm -p 8000:8000 \
      -e API_KEY=SOME_SECRET_TEXT_HERE \
      -e GITHUB_ACCESS_TOKEN=YOUR_PAT_HERE \
      pyrat

## Usage

### Authentication

The `api_key` cookie, header, and/or query argument provides minimal authentication.

### Health
The health check does not require authentication.

http://localhost:8000/healthz

### Swagger Docs

http://localhost:8000/docs?api_token=SOME_SECRET_TEXT_HERE

### List commit messages between two commits or tags

`owner`/`repo`/`base`/`head`/compare

ex. http://localhost:8000/andy-s-clark/pyrat/fd15f34/main/compare?auth_token=SOME_SECRET_TEXT_HERE
