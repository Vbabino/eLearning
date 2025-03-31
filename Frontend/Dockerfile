FROM node:20

WORKDIR /frontend

COPY Frontend/package*.json ./
RUN npm install

COPY Frontend/ ./

RUN npm run build

# Serve with a lightweight HTTP server
RUN npm install -g serve
CMD ["serve", "-s", "dist"]