FROM node:20-alpine
WORKDIR /app

COPY package*.json ./

COPY . .
RUN npm install

ENV PORT=3001
EXPOSE 3001

CMD ["node", "app.js"]

