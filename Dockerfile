# --- Étape 1 : installation des dépendances ---
    FROM python:3.12-slim AS build
    WORKDIR /app
    COPY requirements.txt .
    RUN pip install --no-cache-dir --prefix=/install -r requirements.txt
    
    # --- Étape 2 : image finale, petite et sans root ---
    FROM python:3.12-slim AS runtime
    WORKDIR /app
    COPY --from=build /install /usr/local
    COPY src/ ./src/
    ENV PYTHONPATH=/app/src \
        PYTHONUNBUFFERED=1
    RUN useradd --create-home gazette && mkdir -p /app/data && chown gazette /app/data
    USER gazette
    CMD ["python", "-m", "gazette.flow"]

    # --- Étape 3 : runtime + outils de test (jamais déployée) ---
    FROM runtime AS test
    USER root
    COPY requirements-dev.txt pyproject.toml ./
    RUN pip install --no-cache-dir -r requirements-dev.txt
    COPY tests/ ./tests/
    CMD ["sh", "-c", "ruff check . && pytest -v"]