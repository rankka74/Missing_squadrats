#!/bin/sh
set -e

# Start PHP built-in server as the web frontend
exec php -S 0.0.0.0:8000 -t /srv/www/missing_squadrats \
    -d upload_max_filesize=64M \
    -d post_max_size=64M
