# Copyright (c) 2015 Fabian Kochem


import os


REQUIRED_POSTGRES_VERSION = (9, 4, 0)


def create_schema(cur):
    """ Create table schema. """
    script_folder = os.path.split(os.path.realpath(__file__))[0]
    path = os.path.join(script_folder, '..', 'sql', 'schema.sql')
    cur.execute(open(path).read())


def create_triggers(cur):
    """ Create triggers. """
    script_folder = os.path.split(os.path.realpath(__file__))[0]
    path = os.path.join(script_folder, '..', 'sql', 'triggers.sql')
    cur.execute(open(path).read())


def drop_tables(cur):
    """ Drop all tables. """
    cur.execute("DROP TABLE IF EXISTS nodes;")
    cur.execute("DROP TABLE IF EXISTS ancestors;")


def flush_tables(cur):
    """ Empty all tables. """
    cur.execute("TRUNCATE TABLE nodes RESTART IDENTITY;")
    cur.execute("TRUNCATE TABLE ancestors;")


def is_compatible_postgres_version(cur):
    cur.execute("SHOW server_version;")
    result = cur.fetchone()['server_version']
    server_version = tuple(map(int, result.split('.')))
    return server_version >= REQUIRED_POSTGRES_VERSION
