.. _db_model:

Database Model
==============
`libtree` aims to support billions of nodes while guaranteeing fast
reads and fast writes. Well-known SQL solutions like Adjacency List or
Nested Set have drawbacks which hinder performance in either direction.
The best model to achieve high performance is called `Closure Table`,
which is explained here.


Closure Table
-------------
In Closure Table, you have two tables. One contains the node metadata,
the other one contains every possible ancestor/descendant combination.
In libtree, here's what they look like::

    CREATE TABLE nodes
    (
      id serial NOT NULL,
      parent integer,
      "position" smallint DEFAULT NULL,
      properties jsonb NOT NULL,
      CONSTRAINT "primary" PRIMARY KEY (id)
    )

This is pretty simple and should be self-explanatory. Note that libtree
uses the Adjacency List-style ``parent`` column, even though it's
possible to drag this information out of the ancestor table (see below).
This is mainly for speed reasons as it avoids a JOIN operation onto a
huge table.

The more interesting bit is the ancestor table::

    CREATE TABLE ancestors
    (
      node integer NOT NULL,
      ancestor integer NOT NULL,
      CONSTRAINT idx UNIQUE (node, ancestor)
    )

In this table, every tree relation is stored. This means not only
child/parent, but also grandparent/grandchild relations. So if A is a
parent of B, and B is a parent of C and C is a parent of D, we need to
store the following relations:

+------+----------+
| node | ancestor |
+======+==========+
| A    | B        |
+------+----------+
| A    | C        |
+------+----------+
| A    | D        |
+------+----------+
| B    | C        |
+------+----------+
| B    | D        |
+------+----------+
| C    | D        |
+------+----------+

`(in the real implementation integers are being used)`

This information enables us to query the tree quickly without any form
of recursion. To get the entire subtree of a node, you'd execute
``SELECT ancestor FROM ancestors WHERE node='B'``. Likewise, to get all
ancestors of a node, you'd execute ``SELECT node FROM ancestors WHERE
ancestor='D'``. In both queries you can simply JOIN the nodes table to
retrieve the corresponding metadata. In the second query, you might
notice that the output comes in no particular order, because there is no
column to run SORT BY on. This is an implementation detail of libtree in
order to save disk space and might change at a later point.

Manipulating the tree is somewhat more complex. When inserting a node,
the ancestor information of its parent must be copied and completed.
When deleting a node, all traces of its children must be deleted from
both tables. When moving a node, first all outdated ancestor information
must be found and deleted. Then the new parents ancestor information
must be copied for the node (and its descendants) that is being moved
and completed.

There are different ways to implement Closure Table. Some people store
the depth of each ancestor/descendant combination to make sorting
easier, some don't use the Adjacency List-style `parent` column, and
some even save paths of `length zero` to reduce the complexity of some
queries.


Indices
-------
Everything has tradeoffs; libtree trades speed for disk space. This
means its indices are huge. Both columns in the ancestor table are
indexed separately and together, resulting in index sizes that are twice
the size of the actual data. In the nodes table the columns ``id`` and
``parent`` are indexed, resulting in index sizes that are roughly the
same as the data.

Maybe it's possible to remove indices, this needs benchmarking. But RAM
and disk space became very cheap and doesn't really matter these days,
right? ... right?


Database Triggers
-----------------
The ancestor calculation happens automatically inside PostgreSQL using
trigger functions written in PL/pgSQL. This is great because it means
the user doesn't `have` to use libtree to modify the tree. They can use
their own scripts or manually execute queries from CLI. It's possible
to insert nodes, delete nodes or change the parent attribute of nodes -
the integrity stays intact without the user having to do anything. On
the other hand this means that altering the ancestor table will very
likely result in a broken data set (don't do it).


Referential Integrity
---------------------
While one advantage of using Closure Table is the possibility to use the
RDBMSs referential integrity functionality, libtree doesn't use it in
order to get more speed out of inserts and updates. If the integrity
gets broken somehow, it's simple to fix:

* export nodes table using pgAdmin or similar
* delete both tables
* install libtree again
* import saved nodes table


Boundaries
----------
The ``id`` column is of type ``serial`` (32bit integer) and can
therefore be as high as 2,147,483,647. When needed, changing it t
 ``bigserial`` (64bit integer) is simple but requires more space.


Comparison to other models
--------------------------
**Closure Table**

As mentioned before, Closure Table is a great database model to handle
tree-like data. Its advantages are both read and write performance and
also ease of implementation. It's recursion free and allows you to use
referential integrity. The most complex and slowest part is when
changing parents. Its disadvantage is high disk usage.


**Adjacency List**

The naive and most simple model. All queries and writes are very simple
and fast. It also is referential integrity compatible. However, querying
for nodes any deeper than the immediate children is near impossible
without using recursion on the script side or the rather new WITH
RECURSIVE statement.

**Path Enumeration**

A very good model if you don't mind `stringly typed
<http://neologisms.rice.edu/index.php?a=term&d=1&t=14876>`_ integrity and
tremendous use of string functions in SQL queries. It should be fast for
all types of queries but is not RI-compatible.

**Nested Sets**

Compared to the others, it's very complex and although popular, the
worst model in all ways. It's simple to query subtrees, but it's hard
and slow to do anything else. If you want to insert a node at the top,
you must rebalance the entire tree. If you get the balancing wrong, you
have no chance to repair the hierarchy. Furthermore it's not
RI-compatible.
