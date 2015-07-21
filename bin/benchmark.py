from config import config
from persistance import *
from tree import *
import os
from time import time

if config['mysql']['enabled']:
    conf = config['mysql']
    per = MySQLPersistance(host=conf['host'],
                           user=conf['user'],
                           passwd=conf['password'],
                           db=conf['database'])
else:
    per = PostgreSQLPersistance(config['postgres']['details'])

root = get_root_node(per)
vortec = get_node(per, 154128)
print len(list(get_descendant_ids(per, vortec)))
#print vortec.description
home = get_node(per, 20)
tmp = get_node(per, 9)

start = time()
move_node(per, vortec, tmp)
print time() - start

per.commit()

start = time()
move_node(per, vortec, home)
print time() - start

per.commit()
