libtree
=======

[![Build Status](https://travis-ci.org/conceptsandtraining/libtree.svg?branch=master)](https://travis-ci.org/conceptsandtraining/libtree) [![Documentation Status](https://readthedocs.org/projects/libtree/badge/?version=latest)](http://libtree.readthedocs.org/en/latest/?badge=latest)


**libtree** is a Python library which assists you in dealing with **large, hierarchical data sets**. It runs on top of **PostgreSQL 9.4** and is compatible with Python **2.7, 3.4 and PyPy 3.2**.

Why use **libtree**? Because...

 - the API is **super simple**
 - it scales up to **billions of nodes**
 - the reads and writes are **blazingly fast**
 - it has **attribute inheritance**


But wait, **there’s more**:

 - it doesn’t tell you when to use **transactions**.
 - all tree logic happens **inside the database** and doesn’t occupy your precious CPU.
 - it’s **memory efficient** because **iterators** are being used everywhere where possible.
 - the testsuite covers **>90%** of the code base and is **fully integration tested**.
