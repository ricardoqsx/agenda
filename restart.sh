#!/bin/bash

docker compose down
sudo rm app/*.db
docker system prune -a -f
docker compose up -d
docker compose logs -f