FROM node:22-alpine
WORKDIR /app

# Instala dependências
COPY package.json .
COPY package-lock.json .
RUN npm install

# Copia o código-fonte
COPY . .

# Expõe a porta do Vite
EXPOSE 3000

# Comando para rodar em desenvolvimento (hot-reload)
CMD ["npm", "run", "dev", "--", "--host", "--port", "3000"]