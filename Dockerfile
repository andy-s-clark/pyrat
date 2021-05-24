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

ENV GITHUB_ACCESS_TOKEN=YOUR_PAT_HERE
COPY config ./config
COPY github_compare ./github_compare
COPY app.py .

EXPOSE 5000
CMD ["gunicorn", \
    "--worker-class", "gevent", \
    "--workers", "1", \
    "--bind", "0.0.0.0:5000", \
    "app:app", \
    "--max-requests", "1000", \
    "--timeout", "5", \
    "--keep-alive", "5", \
    "--log-level", "info"]
