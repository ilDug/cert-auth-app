# Stage 1: build di Angular
FROM oven/bun:latest AS frontend-builder
WORKDIR /frontend
COPY frontend/package*.json ./
COPY frontend/bun.lock ./
RUN bun install --frozen-lockfile
COPY frontend/ ./
RUN bun run build


# Stage 2: backend FastAPI + file statici
FROM ghcr.io/astral-sh/uv:alpine
RUN apk add --no-cache openssl
WORKDIR /app
COPY backend/uv.lock ./
COPY backend/pyproject.toml ./
COPY backend/.python-version ./
RUN uv sync  --frozen
COPY backend/ ./

COPY --from=frontend-builder /frontend/dist/ca/browser /app/browser

ENV SECURITY_TOKEN=NOT_SET

VOLUME ["/app/PKI"]
EXPOSE 8000
CMD ["uv",  "run", "fastapi", "run", "app/main.py", "--proxy-headers", "--port", "8000"]


# USAGE
# Build the Docker image
# docker build -t cert-auth:latest .

# Run the Docker container
# docker run -p 8000:8000 -v ./PKI:/app/PKI --env MODE=PRODUCTION --env SECURITY_TOKEN="ciaiciaicaiciaicia" cert-auth:latest