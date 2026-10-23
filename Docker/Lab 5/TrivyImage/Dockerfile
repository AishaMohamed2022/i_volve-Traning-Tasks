FROM node:20-alpine

WORKDIR /app

COPY package*.json ./

RUN npm install --only=production

COPY app.js ./

# Enforce non-root execution using built-in node user
USER node

EXPOSE 3000

CMD ["npm", "start"]