FROM node:20-alpine
WORKDIR /app

COPY package*.json ./

COPY . .
RUN npm install

ENV PORT=3002
EXPOSE 3002

CMD ["node", "app.js"]

