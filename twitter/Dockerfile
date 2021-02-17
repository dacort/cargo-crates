# For more information, please refer to https://aka.ms/vscode-docker-python
FROM python:3.8-slim-buster

# We need to provide OAuth 1.0a Credentials
ENV CONSUMER_KEY=
ENV CONSUMER_SECRET=
ENV ACCESS_TOKEN_KEY=
ENV ACCESS_TOKEN_SECRET=

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
ENTRYPOINT ["python", "twitter.py"]
