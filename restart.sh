#!/bin/bash

docker compose down
docker system prune -a -f
docker compose up -d
docker compose logs -f