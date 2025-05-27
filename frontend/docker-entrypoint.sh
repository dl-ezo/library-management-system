#!/bin/sh
set -e

# Copy the nginx config directly (no templating needed now)
cp /etc/nginx/conf.d/default.conf.template /etc/nginx/conf.d/default.conf

exec nginx -g 'daemon off;'
