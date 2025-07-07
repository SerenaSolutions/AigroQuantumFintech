
# Use a imagem oficial do Node.js para construir o frontend
FROM node:18-alpine as builder

WORKDIR /app

# Copia os arquivos de dependências e instala
COPY package.json package-lock.json ./
RUN npm install

# Copia o restante do código e constrói o aplicativo
COPY . .
RUN npm run build

# Use uma imagem leve para servir o aplicativo
FROM nginx:alpine

COPY --from=builder /app/build /usr/share/nginx/html

EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
