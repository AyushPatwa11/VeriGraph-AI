FROM node:18-alpine AS base

WORKDIR /app

COPY package*.json ./
RUN npm ci

COPY . .

ENV NEXT_TELEMETRY_DISABLED=1
RUN npm run build

EXPOSE 3000
CMD ["npm", "run", "start"]
