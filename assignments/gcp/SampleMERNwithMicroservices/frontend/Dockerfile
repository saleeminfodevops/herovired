FROM node:20-alpine
WORKDIR /app
ENV PORT=3000
ENV HOST=0.0.0.0
EXPOSE 3000
COPY package*.json ./
RUN npm install
COPY . .
CMD ["npm","start","--","--host","0.0.0.0"]
