# Usar a mesma imagem base do backend para consistência
FROM python:3.11-slim

# Definir o diretório de trabalho
WORKDIR /app

# Copiar o arquivo de dependências da pasta 'backend' e instalar
COPY ./requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiar apenas as pastas e arquivos necessários para o teste
COPY ./database.py .
COPY ./utils ./utils
COPY ./services ./services
COPY ./models ./models
COPY ./performance_tests ./performance_tests