# Production web Dockerfile. This is a multi-step docker image
#
# Note that there is no development web Dockerfile. You will need to run the
# devserver locally. Detailed instructions for that are given in /web

########## FIRST STEP: FRONTEND BUILD #######
FROM node:16 as frontendbuild

WORKDIR /frontend

#first, we copy the package.json and install the dependencies
COPY web/package*.json ./
RUN npm ci

#then we copy the codebase and build it. If there are no changes to the
#package json, the installation proces will be cached in a layer
COPY web/ .
RUN npm run build

########## FINAL STEP: PRODUCTION IMAGE #######
FROM nginx

#copy the frondend files generated in the previous step
COPY --from=frontendbuild /frontend/dist /usr/share/nginx/html

#remove base nginx configuration files
RUN rm /etc/nginx/conf.d/default.conf
#copy our nginx configuration files
COPY docker/web/custom.conf /etc/nginx/conf.d/nginx.conf
