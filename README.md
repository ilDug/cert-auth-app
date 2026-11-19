# cert-auth-app

[![build & test](https://github.com/ilDug/cert-auth-app/actions/workflows/test.yaml/badge.svg)](https://github.com/ilDug/cert-auth-app/actions/workflows/test.yaml)
[![Build images e Deploy](https://github.com/ilDug/cert-auth-app/actions/workflows/deploy.yaml/badge.svg)](https://github.com/ilDug/cert-auth-app/actions/workflows/deploy.yaml)
![Latest Release](https://img.shields.io/github/v/release/ilDug/cert-auth-app?display_name=tag&include_prereleases)

Certification authority application for managing local certificate.

## Run docker container

Use the image built from the Dockerfile to run the container. 

```bash
docker pull ghcr.io/ildug/cert-auth-app:latest
```


The application needs a folder to store the entre PKI structure. Make sure to create a directory on your host machine and mount it to the container when running it.
Expose the port 8000 to access the application from your host machine.

```bash
mkdir -p /path/to/PKI

docker run -d \
  -p 8000:8000 \
  -v /path/to/pki:/app/pki \
  ghcr.io/ildug/cert-auth-app:latest
```