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

COPY ./app .

EXPOSE 8000
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
