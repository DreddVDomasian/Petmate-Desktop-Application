
# SHORTCUT TO UPDATE THE DOCKER IMAGE
# docker run --rm -d -p 8080:80 --name petmate-container petmate-web

#   docker stop petmate-container
#   docker rm petmate-container

FROM nginx:alpine

# Remove default nginx files
RUN rm -rf /usr/share/nginx/html/*

# Copy your site files while preserving "html" folder
COPY ./html /usr/share/nginx/html/html

# Copy css, js, and assets into their own folders
COPY ./css /usr/share/nginx/html/css
COPY ./js /usr/share/nginx/html/js
COPY ./assets /usr/share/nginx/html/assets

EXPOSE 80