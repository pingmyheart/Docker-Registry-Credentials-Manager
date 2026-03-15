# Docker-Registry-Credentials-Manager

*Automated Credential Management for Docker Registries*

![Last Commit](https://img.shields.io/github/last-commit/pingmyheart/Docker-Registry-Credentials-Manager)
![Repo Size](https://img.shields.io/github/repo-size/pingmyheart/Docker-Registry-Credentials-Manager)
![Issues](https://img.shields.io/github/issues/pingmyheart/Docker-Registry-Credentials-Manager)
![Pull Requests](https://img.shields.io/github/issues-pr/pingmyheart/Docker-Registry-Credentials-Manager)
![License](https://img.shields.io/github/license/pingmyheart/Docker-Registry-Credentials-Manager)
![Top Language](https://img.shields.io/github/languages/top/pingmyheart/Docker-Registry-Credentials-Manager)
![Language Count](https://img.shields.io/github/languages/count/pingmyheart/Docker-Registry-Credentials-Manager)

## 🚀 Overview

This project provides a secure and automated solution for managing credentials for private Docker registries. It allows
registry manager to easily generate and distribute temporary access to users, ensuring secure and efficient
access to private Docker images.

## ✨ Features

- 🔐 **User Creation:** Create users with unique usernames and passwords.
- 🔐 **User Deletion:** Delete users when access is no longer needed.
- 🔒 **Secure Credential Storage:** Store credentials securely in a htpasswd file shared with registry config.

## 🛠️ Getting Started

### Prerequisites

- Docker
- Docker Compose

### Installation

#### Native Installation

1. Clone the repository

```bash
git clone https://github.com/pingmyheart/Docker-Registry-Credentials-Manager.git
cd Docker-Registry-Credentials-Manager
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python3 app.py
```

2. Set up environment variables

```bash
HTPASSWD_FILE_PATH=../registry/auth/htpasswd
```

#### Docker Installation

1. Pull the docker image

```bash
docker pull ghcr.io/pingmyheart/docker-registry-credentials-manager:${VERSION}
```

2. Run the container

```yaml
services:
  registry:
    image: registry:2
    container_name: registry
    ports:
      - "5000:5000"
    volumes:
      - registry-data:/var/lib/registry
      - ./auth:/auth
      - ./config.yml:/etc/docker/registry/config.yml
    restart: always
    environment:
      - "REGISTRY_AUTH=htpasswd"
      - "REGISTRY_AUTH_HTPASSWD_REALM=Registry Realm"
      - "REGISTRY_AUTH_HTPASSWD_PATH=/auth/htpasswd"
  py-cert-server:
    image: ghcr.io/pingmyheart/docker-registry-credentials-manager:${VERSION}
    environment:
      - HTPASSWD_FILE_PATH=/registry/auth/htpasswd
    volumes:
      - ./auth:/registry/auth
    ports:
      - "8080:8080"
volumes:
  registry-data:
    name: registry_data
```

with config file

```yaml
version: 0.1
loglevel: debug
storage:
  filesystem:
    rootdirectory: /var/lib/registry
  delete:
    enabled: true
http:
  addr: 0.0.0.0:5000
auth:
  htpasswd:
    realm: Registry Realm
    path: /auth/htpasswd

```

## 📚 Usage

### Create new user

```bash
curl --location 'localhost:5000/credential/users/mysuperusername' \
--header 'Content-Type: application/json' \
--data-raw '{
    "username": "mysuperusername",
    "password": "mysuperpassword"
}'
```

### Delete user

```bash
curl --location --request DELETE 'localhost:5000/credential/users/mysuperusername' \
--header 'Content-Type: application/json' \
```

### List users

```bash
curl --location --request GET 'localhost:5000/credential/users' \
--header 'Content-Type: application/json' \
```