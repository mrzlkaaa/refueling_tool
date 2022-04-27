FROM node:lts-alpine as build-stage
# FROM node:lts-alpine
# RUN npm install -g http-server
WORKDIR /frontend
COPY package*.json ./
RUN npm install
COPY . .
RUN npm run build
# CMD [ "http-server", "dist" ]

# # production stage
FROM nginx:stable-alpine as production-stage
COPY --from=build-stage /frontend/dist /usr/share/nginx/html
COPY --from=build-stage /frontend/src/assets /usr/share/nginx/html/assets
COPY conf /etc/nginx/conf.d/default.conf
COPY /ssl_cert /etc/nginx/certs
CMD ["nginx", "-g", "daemon off;"]