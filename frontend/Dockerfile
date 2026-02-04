FROM alpine:latest
RUN mkdir /app
WORKDIR /app
RUN apk add nodejs npm
COPY . /app
RUN npm install
EXPOSE 3000
CMD ["node", "app.js"]