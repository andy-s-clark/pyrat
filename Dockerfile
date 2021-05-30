FROM python:3.8-slim

# Add Python user
RUN adduser --uid 1001 --system pythonrole \
    && mkdir -p /opt/app \
    && chown -R pythonrole /opt/app

USER pythonrole

ENV VIRTUAL_ENV=/opt/app/venv
RUN python3 -m venv $VIRTUAL_ENV
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

WORKDIR /opt/app
COPY requirements.txt .
RUN pip install -r requirements.txt
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

COPY config ./config
COPY github_compare ./github_compare
COPY app.py .

ENV API_KEY=SOME_SECRET_TEXT_HERE
ENV GITHUB_ACCESS_TOKEN=YOUR_PAT_HERE
ENV JIRA_API_TOKEN=YOUR_JIRA_API_TOKEN
ENV JIRA_URL=https://jira.atlassian.com
ENV JIRA_USERNAME=YOUR_JIRA_USERNAME
ENV PORT=8000
EXPOSE $PORT
CMD uvicorn app:app --host 0.0.0.0 --port ${PORT}
