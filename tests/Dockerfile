# Usar a mesma base do backend para consistência
FROM python:3.11-slim

WORKDIR /app

# Instalar dependências de teste
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiar os scripts de teste
COPY . .

# O comando padrão será rodar o pytest
CMD ["pytest", "-v"]