# Copyright (c) 2015 Fabian Kochem


from libtree.config import config
from pdb import set_trace as trace
from libtree.persistence import *
import os
from libtree.tree import *

per = PostgreSQLPersistence(config['postgres']['details'])
cache = {}

per.drop_tables()
per.create_schema()
per.commit()

start_path = '/'
root = insert_node(per, None, 'folder')
cache[start_path] = root.id

for dirname, folders, files in os.walk(start_path):
    for folder in folders:
        path = os.path.join(dirname, folder)
        #print path
        parent = cache[dirname]
        node = insert_node(per, parent, 'folder')
        cache[path] = node.id

    for filex in files:
        path = os.path.join(dirname, filex)
        #print path
        parent = cache[dirname]
        node = insert_node(per, parent, 'file')
        cache[path] = node.id

    db.commit()

#trace()
