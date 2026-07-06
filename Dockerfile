FROM php:8.4-cli-alpine

ARG MKGMAP_VERSION=r4924

# System dependencies (Alpine)
RUN apk add --no-cache \
    openjdk21-jre-headless \
    py3-shapely \
    python3 \
    unzip \
    wget

# Directory structure that matches the relative paths in the Python scripts:
#   script_dir = /srv/src/missing_squadrats/
#   script_dir + ../../jobs/... = /srv/jobs/missing_squadrats/
#   script_dir + ../../www/...  = /srv/www/missing_squadrats/
#   Path(__file__).parent^3 / YYYYMMDD = /srv/YYYYMMDD/  (temp build dir)
#   logFilePath = /home/users/oranta/  (hardcoded)
RUN mkdir -p \
    /srv/src/ext \
    /srv/src/missing_squadrats \
    /srv/jobs/missing_squadrats \
    /srv/www/missing_squadrats/img \
    /home/users/oranta/python3/venv/bin \
    /var/www/10/oranta/sites/oranta.kapsi.fi

# Download mkgmap and symlink to the version hardcoded in missing_squadrats.py
RUN wget -q "https://www.mkgmap.org.uk/download/mkgmap-${MKGMAP_VERSION}.zip" \
    && unzip -q "mkgmap-${MKGMAP_VERSION}.zip" -d /srv/src/ext/ \
    && rm "mkgmap-${MKGMAP_VERSION}.zip" \
    && ln -s "/srv/src/ext/mkgmap-${MKGMAP_VERSION}" /srv/src/ext/mkgmap-r4916

# Symlinks for the two hardcoded absolute paths in the Python scripts
RUN ln -s /srv/jobs /var/www/10/oranta/sites/oranta.kapsi.fi/jobs \
    && ln -s /usr/bin/python3 /home/users/oranta/python3/venv/bin/python3

# Seed mapName.txt so the script has a valid starting map number
RUN echo "2026-01-01 00:00:00,17,0,63040001" > /home/users/oranta/mapName.txt \
    && touch /home/users/oranta/missingSquadrats.log

EXPOSE 8000

COPY docker-entrypoint.sh /usr/local/bin/docker-entrypoint.sh
RUN chmod +x /usr/local/bin/docker-entrypoint.sh

ENTRYPOINT ["docker-entrypoint.sh"]
