FROM node:16-alpine as build-stage
WORKDIR /app
COPY /src ./
COPY . .
RUN npm install
RUN npm run serve

FROM nginx as production-stage
RUN mkdir /app
COPY --from=build-stage /app/dist /app
COPY nginx.conf /etc/nginx/nginx.conf