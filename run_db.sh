#!/bin/bash

docker run --rm -d --network host --name pg-zbd5 -e POSTGRES_PASSWORD=docker postgres

sleep 5;

PGPASSWORD=docker psql -h localhost -p 5432 -U postgres -c 'CREATE DATABASE zbd5';

./setup_db.py

npx postgraphile -c 'postgres://postgres:docker@localhost:5432/zbd5' --watch --enhance-graphiql

docker stop pg-zbd5
