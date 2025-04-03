FROM node:18-alpine

WORKDIR /frontend

COPY package.json .
RUN npm install

RUN npm i -g serve

COPY . . 

RUN npm run build

EXPOSE 3000

# Serve with a lightweight HTTP server
RUN npm install -g serve
CMD ["serve", "-s", "dist"]