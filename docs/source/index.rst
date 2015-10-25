.. _index:

Welcome to libtree's documentation!
===================================

**libtree** is a Python library which assists you in dealing with
**large, hierarchical data sets**. It runs on top of **PostgreSQL 9.4**
and is compatible with **all major Python interpreters** (2.7, 3.3-3.5, PyPy2
and PyPy3).

Why use **libtree**? Because...

* the usage is **super simple** (see :ref:`quickstart`)
* it scales up to **billions of nodes** (see :ref:`db_model`)
* the reads and writes are **blazingly fast** (:ref:`benchmarks` will be
  available soon)
* it supports **attribute inheritance** (see :ref:`coreapi-properties`)

But there's even more, **libtree**...

* offers **thread-safety** by working inside transactions
* enforces **integrity** by moving tree logic to inside the database
* provides a **convenient** high level API and **fast** low level functions
* core is **fully integration tested**, the testsuite covers >90% of the code


Contents
========

.. toctree::
   :maxdepth: 2

   installation
   quickstart
   user_guide
   publicapi/index
   coreapi/index
   benchmarks
   db_model

* :ref:`genindex`
