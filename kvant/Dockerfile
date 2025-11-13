# Многоэтапная сборка для фронтенда
FROM node:20-alpine AS build

# Установка рабочей директории
WORKDIR /app

# Копирование package.json и package-lock.json
COPY package*.json ./

# Установка зависимостей (включая dev для сборки)
RUN npm ci

# Копирование исходного кода
COPY . .

# Сборка приложения
RUN npm run build

# Production образ
FROM nginx:alpine AS production

# Копирование собранного приложения
COPY --from=build /app/dist /usr/share/nginx/html

# Копирование кастомной конфигурации nginx
COPY nginx.conf /etc/nginx/nginx.conf

# Экспорт порта
EXPOSE 80

# Запуск nginx
CMD ["nginx", "-g", "daemon off;"]

# Development образ
FROM node:20-alpine AS development

WORKDIR /app

# Копирование package.json и установка зависимостей
COPY package*.json ./
RUN npm install

# Копирование исходного кода
COPY . .

# Экспорт порта для dev сервера
EXPOSE 5173

# Запуск dev сервера
CMD ["npm", "run", "dev", "--", "--host", "0.0.0.0"]
