# Multi-stage Dockerfile for backend (FastAPI) and frontend (Vite/React)

# Backend build stage
FROM python:3.11-slim AS backend-build
WORKDIR /backend
COPY ./backend/requirements.txt ./requirements.txt
RUN pip install --no-cache-dir -r requirements.txt
COPY ./backend/app ./app

# Frontend build stage
FROM node:18-alpine AS frontend-build
WORKDIR /frontend
COPY ./frontend/package.json ./package.json
COPY ./frontend/package-lock.json ./package-lock.json
RUN npm install --legacy-peer-deps || yarn install --frozen-lockfile
COPY ./frontend .
RUN npm run build || yarn build

# Final stage: serve both
FROM python:3.11-slim AS final
WORKDIR /code

# Copy backend from backend-build
COPY --from=backend-build /backend/app ./app
COPY --from=backend-build /backend/requirements.txt ./requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy frontend build output
COPY --from=frontend-build /frontend/dist ./frontend_dist

# Expose ports
EXPOSE 8000
EXPOSE 3000

# Start backend (FastAPI)
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]

# To serve frontend, add a simple static server or use nginx in another container
