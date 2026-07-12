FROM node:20-alpine
WORKDIR /app

COPY package*.json ./

COPY . .
RUN npm install

ENV PORT=3003
EXPOSE 3003

CMD ["node", "app.js"]

