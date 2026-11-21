FROM nginx:alpine
COPY ./index.html /usr/share/nginx/html/index.html
COPY ./404.html /usr/share/nginx/html/404.html
COPY ./script.js /usr/share/nginx/html/script.js
COPY ./style.css /usr/share/nginx/html/style.css
COPY ./nginx.conf /etc/nginx/conf.d/default.conf
EXPOSE 80