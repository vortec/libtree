# Copyright (c) 2016 Fabian Kochem


import os


REQUIRED_POSTGRES_VERSION = (9, 5, 0)


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
    """
    Determine whether PostgreSQL server version is compatible with
    libtree.
    """
    cur.execute("SHOW server_version;")
    result = cur.fetchone()['server_version']
    server_version = tuple(map(int, result.split('.')))
    return server_version >= REQUIRED_POSTGRES_VERSION


def make_dsn_from_env(env):
    """
    Make DSN string from libpq environment variables.
    """
    ret = []
    mapping = {
        'PGHOST': 'host',
        'PGPORT': 'port',
        'PGUSER': 'user',
        'PGPASSWORD': 'password',
        'PGDATABASE': 'dbname'
    }

    for env_name in ('PGHOST', 'PGPORT', 'PGUSER', 'PGPASSWORD', 'PGDATABASE'):
        value = env.get(env_name)
        if value:
            dsn_name = mapping[env_name]
            ret.append('{}={}'.format(dsn_name, value))

    return ' '.join(ret)
