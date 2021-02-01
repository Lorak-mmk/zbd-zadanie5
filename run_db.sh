#!/bin/bash
set -e

function cleanup() {
    docker stop pg-zbd5
}

trap cleanup EXIT

docker run --rm -d --network host --name pg-zbd5 -e POSTGRES_PASSWORD=docker postgres
sleep 5;
PGPASSWORD=docker psql -h localhost -p 5432 -U postgres -c 'CREATE DATABASE zbd5';
./setup_db.py

DATABASE_URL='postgres://postgres:docker@localhost:5432/zbd5' node run_db.js
