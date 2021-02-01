#!/usr/bin/env python

import psycopg2


HOST='localhost'
USER='postgres'
PASSWORD='docker'

create_table_users = '''
    CREATE TABLE users (
        id CHAR(32) PRIMARY KEY,
        born_year INTEGER,
        income BIGINT,
        lat DOUBLE PRECISION,
        lon DOUBLE PRECISION
    )
'''

create_table_interests = '''
    CREATE TABLE interests (
        id SERIAL PRIMARY KEY,
        user_id CHAR(32) REFERENCES users(id) NOT NULL,
        name VARCHAR(64) NOT NULL,
        UNIQUE(user_id, name)
    )
'''

create_table_ads = '''
    CREATE TABLE ads (
        id CHAR(32) PRIMARY KEY,
        height INTEGER,
        width INTEGER,
        color CHAR(7)
    )
'''

create_table_ads_texts = '''
    CREATE TABLE ads_texts (
        id SERIAL PRIMARY KEY,
        ad_id CHAR(32) REFERENCES ads(id) NOT NULL,
        name VARCHAR(64) NOT NULL,
        UNIQUE(ad_id, name)
    )
'''

create_table_views = '''
    CREATE TABLE views (
        id SERIAL PRIMARY KEY,
        user_id CHAR(32) REFERENCES users(id) NOT NULL,
        ad_id CHAR(32) REFERENCES ads(id) NOT NULL,
        time TIMESTAMPTZ NOT NULL
    )
'''

insert_interests = '''
    CREATE FUNCTION insert_interests(uid CHAR(32), intr VARCHAR(64)[])
    RETURNS VOID
    AS $$
        DELETE FROM "interests"
        WHERE "user_id" = uid;
        INSERT INTO "interests" ("user_id", "name")
        SELECT uid, n
        FROM unnest(intr) n;
    $$ LANGUAGE sql VOLATILE;
'''

insert_ad_texts = '''
    CREATE FUNCTION insert_ad_texts(ad_id CHAR(32), texts VARCHAR(64)[])
    RETURNS VOID
    AS $$
        DELETE FROM "ads_texts"
        WHERE "ad_id" = ad_id;
        INSERT INTO "ads_texts" ("ad_id", "name")
        SELECT ad_id, n
        FROM unnest(texts) n;
    $$ LANGUAGE sql VOLATILE;
'''



table_queries = [
    create_table_users,
    create_table_interests,
    create_table_ads,
    create_table_ads_texts,
    create_table_views,
    insert_interests,
    insert_ad_texts
]

def main():
    conn = psycopg2.connect(host=HOST, user=USER, password=PASSWORD, dbname='zbd5')
    conn.set_isolation_level(psycopg2.extensions.ISOLATION_LEVEL_AUTOCOMMIT)
    curs = conn.cursor()
    for query in table_queries:
        curs.execute(query)


if __name__ == '__main__':
    main()
