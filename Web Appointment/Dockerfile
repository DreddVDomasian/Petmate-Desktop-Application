
# SHORTCUT TO UPDATE THE DOCKER IMAGE
#   docker stop petmate-container   1
#   docker rm petmate-container     2
# docker run --rm -d -p 8080:80 --name petmate-container petmate-web    3


FROM nginx:alpine

# Remove default nginx files
RUN rm -rf /usr/share/nginx/html/*

# Copy site files into nginx html folder
COPY ./html/ /usr/share/nginx/html/
COPY ./css /usr/share/nginx/html/css
COPY ./js /usr/share/nginx/html/js
COPY ./assets /usr/share/nginx/html/assets
COPY ./data /usr/share/nginx/html/data

# Copy custom nginx config
COPY default.conf /etc/nginx/conf.d/default.conf

EXPOSE 80



