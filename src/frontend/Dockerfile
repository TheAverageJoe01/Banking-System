FROM node:21.6.2-alpine as build
WORKDIR /frontend
COPY package*.json ./
RUN npm install
COPY . .
RUN npm run build
FROM nginx:1.21.3-alpine
COPY --from=build /frontend/build /usr/share/nginx/html
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]