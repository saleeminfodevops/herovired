FROM node:20-alpine
WORKDIR /app
ENV PORT=3002
ENV HOST=0.0.0.0
ENV MONGO_URL=mongodb+srv://vivekreddyainala_db_user:India@mern-app-db.ar1apep.mongodb.net/MERN_DB
EXPOSE 3002
COPY package*.json .
RUN npm install
COPY . .
CMD ["node","index.js"]
