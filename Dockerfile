FROM python:3.12-slim

# Avoid prompts from apt
ENV DEBIAN_FRONTEND=noninteractive

# Install system dependencies and Node.js
RUN apt-get update && apt-get install -y \
    git \
    curl \
    ca-certificates \
    && curl -fsSL https://deb.nodesource.com/setup_20.x | bash - \
    && apt-get install -y nodejs \
    && rm -rf /var/lib/apt/lists/*

# Copy agent folder
COPY agent /agent

# Install dependencies
WORKDIR /agent
RUN pip install --no-cache-dir -r requirements.txt

# Install npm dependencies (Claude CLI)
RUN npm install

# Use absolute path since GitHub Actions overrides workdir
ENTRYPOINT ["python", "/agent/entrypoint.py"]