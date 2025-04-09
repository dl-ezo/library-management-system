# Multi-stage build for the library management system

# Stage 1: Build frontend
FROM node:18 as frontend-builder
WORKDIR /app/frontend
COPY frontend/package*.json ./
RUN npm install
COPY frontend/ ./
RUN npm run build

# Stage 2: Build backend
FROM python:3.12-slim as backend-builder
WORKDIR /app/backend
RUN pip install poetry
COPY backend/pyproject.toml backend/poetry.lock ./
RUN poetry config virtualenvs.create false && \
    poetry install --without dev --no-root --no-interaction --no-ansi

# Stage 3: Final image
FROM python:3.12-slim
WORKDIR /app
RUN pip install poetry

# Copy backend files
COPY --from=backend-builder /usr/local/lib/python3.12/site-packages /usr/local/lib/python3.12/site-packages
COPY backend/ /app/backend/

# Create static directory and copy frontend build
RUN mkdir -p /app/backend/static
COPY --from=frontend-builder /app/frontend/dist/ /app/backend/static/

# Set working directory to backend
WORKDIR /app/backend

# Install poetry, uvicorn globally, and create a proper environment
RUN pip install --no-cache-dir poetry uvicorn[standard] && \
    cd /app/backend && \
    poetry config virtualenvs.create false && \
    poetry install --without dev --no-root --no-interaction

# Run the application using global uvicorn instead of poetry run
CMD ["sh", "-c", "cd /app/backend && uvicorn app.main:app --host 0.0.0.0 --port ${PORT:-8000}"]
