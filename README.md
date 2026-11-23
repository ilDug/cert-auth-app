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


The application needs a folder to store the entre PKI structure. Make sure to create a directory on your host machine and mount it on `/app/PKI` to the container when running it.
Expose the port 8000 to access the application from your host machine.

```bash
mkdir -p /path/to/pki

docker run -d \
  --publish 8000:8000 \
  --volume /path/to/pki:/app/PKI \
  --volume /etc/localtime:/etc/localtime:ro \
  --env MODE=PRODUCTION \
  --env TZ=Europe/Rome \
  --env SECURITY_TOKEN=$(openssl rand -hex 32) \
  --network proxy \
  ghcr.io/ildug/cert-auth-app:latest
```

## Run behind a reverse proxy

When running the application behind a reverse proxy, make sure to configure the proxy to forward the appropriate headers and to use the correct port mapping. The application should be accessible through the proxy at the configured domain and port.

### Example traefik configuration

```bash 
docker run -d \
  --publish 8000:8000 \
  --volume /path/to/pki:/app/PKI \
  --volume /etc/localtime:/etc/localtime:ro \
  --network proxy \
  --env MODE=PRODUCTION \
  --env TZ=Europe/Rome \
  --env SECURITY_TOKEN=$(openssl rand -hex 32) \
  --label "traefik.enable=true" \
  --label "traefik.http.routers.cert-auth-app.rule=Host(\`ca.example.com\`)" \
  --label "traefik.http.routers.cert-auth-app.tls=true" \
  --label "traefik.http.routers.cert-auth-app.entrypoints=websecure" \
  --label "traefik.http.routers.cert-auth-app.service=cert-auth-app" \
  --label "traefik.http.routers.cert-auth-app.middlewares=basic_auth@file" \
  --label "traefik.http.services.cert-auth-app.loadbalancer.server.port=8000" \
  --label "traefik.http.services.cert-auth-app.loadbalancer.healthcheck.path=/health-check" \
  ghcr.io/ildug/cert-auth-app:latest
```

or run a a **service** 

```bash 
docker service create \
  --name cert-auth-app \
  --publish 8000:8000 \
  --replicas 1 \
  --mount type=bind,source=/path/to/pki,target=/app/PKI \
  --mount type=bind,source=/etc/localtime,target=/etc/localtime,readonly \
  --env MODE=PRODUCTION \
  --env TZ=Europe/Rome \
  --env SECURITY_TOKEN=$(openssl rand -hex 32) \
  --network proxy \
  --label "traefik.enable=true" \
  --label "traefik.http.routers.cert-auth-app.rule=Host(\`ca.example.com\`)" \
  --label "traefik.http.routers.cert-auth-app.tls=true" \
  --label "traefik.http.routers.cert-auth-app.entrypoints=websecure" \
  --label "traefik.http.routers.cert-auth-app.service=cert-auth-app" \
  --label "traefik.http.routers.cert-auth-app.middlewares=basic_auth@file" \
  --label "traefik.http.services.cert-auth-app.loadbalancer.server.port=8000" \
  --label "traefik.http.services.cert-auth-app.loadbalancer.healthcheck.path=/health-check" \
  ghcr.io/ildug/cert-auth-app:latest
```