#!/bin/sh
rm volumes/traefik/acme/acme.json
rm volumes/traefik/logs/traefik.log
touch volumes/traefik/acme/acme.json
chmod 600 volumes/traefik/acme/acme.json
touch volumes/traefik/logs/traefik.log