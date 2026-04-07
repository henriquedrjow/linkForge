# Dockerfile
FROM python:3.9-slim AS builder

WORKDIR /app

RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir poetry

COPY pyproject.toml poetry.lock ./

RUN poetry config virtualenvs.create false && \
    poetry install --no-dev --no-interaction --no-ansi

COPY . .

# Build the wheel package
RUN poetry build -f wheel

# --- Production Stage ---
FROM python:3.9-slim

WORKDIR /app

# Copy only the built wheel file from the builder stage
COPY --from=builder /app/dist/*.whl /app/
RUN pip install --no-cache-dir /app/*.whl && \
    rm -rf /app/*.whl

# Expose the port the app runs on
EXPOSE 8000

# Command to run the application using Uvicorn
# Use a production-ready server like Uvicorn with multiple workers in a real deployment
CMD ["uvicorn", "linkforge.main:app", "--host", "0.0.0.0", "--port", "8000"]