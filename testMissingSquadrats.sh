#!/usr/bin/bash

if [ -f /var/www/10/oranta/sites/oranta.kapsi.fi/src/missing_squadrats/runMissingSquadrats.sh ]; then
    date  >> /home/users/oranta/missingSquadrats.log
    sh /var/www/10/oranta/sites/oranta.kapsi.fi/src/missing_squadrats/runMissingSquadrats.sh >> /home/users/oranta/missingSquadrats.log 2>&1
	rm /var/www/10/oranta/sites/oranta.kapsi.fi/src/missing_squadrats/runMissingSquadrats.sh
fi
