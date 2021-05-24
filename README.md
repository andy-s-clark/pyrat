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
    export GITHUB_ACCESS_TOKEN=YOUR_PAT_HERE
    python app.py

## Docker

    docker build -t pyrat .
    docker run -it --name pyrat --rm -p 5000:5000 \
      -e GITHUB_ACCESS_TOKEN=YOUR_PAT_HERE \
      pyrat

## Usage

### List commit messages between two commits or tags

`owner`/`repo`/`base`/`head`/compare

ex. http://localhost:5000/andy-s-clark/pyrat/fd15f34/main/compare
