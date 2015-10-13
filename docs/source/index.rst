.. _index:

Welcome to libtree's documentation!
===================================

**libtree** is a Python library which assists you in dealing with
**large, hierarchical data sets**. It runs on top of **PostgreSQL 9.4**
and is compatible with **all major Python interpreters** (2.7, 3.3-3.5, PyPy2
and PyPy3).

Why use **libtree**? Because...

* the API is **super simple** (see :ref:`api`)
* it scales up to **billions of nodes** (see :ref:`db_model`)
* the reads and writes are **blazingly fast** (:ref:`benchmarks` will be
  available soon)
* it has **attribute inheritance** (see :ref:`api-properties`)

But wait, **there's more**:

* it doesn't tell you when to use **transactions**.
* all tree logic happens **inside the database** and doesn't occupy your
  precious CPU.
* it's **memory efficient** because **iterators** are being used
  everywhere where possible.
* the testsuite covers **>90%** of the code base and is **fully integration
  tested**.


Contents
========

.. toctree::
   :maxdepth: 2

   installation
   quickstart
   user_guide
   api/index
   benchmarks
   db_model

* :ref:`genindex`
