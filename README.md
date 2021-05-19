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

    cd app
    export GITHUB_ACCESS_TOKEN=YOUR_PAT_HERE
    uvicorn main:app --reload

### Swagger Docs
http://127.0.0.1:8000/docs

## Docker

    docker build -t pyrat .
    docker run -it --name pyrat --rm -p 8000:8000 \
      -e GITHUB_ACCESS_TOKEN=YOUR_PAT_HERE \
      pyrat
