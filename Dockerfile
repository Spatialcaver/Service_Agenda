FROM python:3.12-slim

# Impede que o Python gere arquivos .pyc e permite logs em tempo real
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /app

# Dependências para o PostgreSQL
RUN apt-get update && apt-get install -y libpq-dev gcc && rm -rf /var/lib/apt/lists/*

# Copia os requisitos (certifique-se de que corrigiu o arquivo no passo 2)
COPY requiriments.txt .
RUN pip install --no-cache-dir -r requiriments.txt

COPY . .

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]