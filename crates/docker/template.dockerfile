# For more information, please refer to https://aka.ms/vscode-docker-python
FROM python:3.8-slim-buster

LABEL org.opencontainers.image.source https://github.com/dacort/cargo-crates

# We need to provide a personal access token
$env

# We can configure various output mechanisms - default is stdout
ENV OUTPUT_TYPE=stdout
ENV OUTPUT_PARAMS={}

# Keeps Python from generating .pyc files in the container
ENV PYTHONDONTWRITEBYTECODE=1

# Turns off buffering for easier container logging
ENV PYTHONUNBUFFERED=1

# Install pip requirements
COPY requirements.txt .
RUN python -m pip install -r requirements.txt

WORKDIR /app
COPY . /app

# Switching to a non-root user, please refer to https://aka.ms/vscode-docker-python-user-rights
RUN useradd appuser && chown -R appuser /app
USER appuser

# During debugging, this entry point will be overridden. For more information, please refer to https://aka.ms/vscode-docker-python-debug
COPY --from=ghcr.io/dacort/forklift:latest /forklift /usr/local/bin/forklift
ENTRYPOINT $entry
