# ── Build leve: Python 3.12 slim (sem Nix, sem gcc desnecessário) ──
FROM python:3.12-slim

# Evita prompts interativos durante o build
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

WORKDIR /app

# Copia só o requirements primeiro (aproveita cache do Docker)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copia o resto do projeto
COPY . .

# Porta exposta
EXPOSE 8000

# Inicia com 1 worker para economizar memória
CMD ["gunicorn", "condominio:app", "--bind", "0.0.0.0:8000", "--workers", "1", "--timeout", "120"]