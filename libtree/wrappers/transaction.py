# Copyright (c) 2015 Fabian Kochem


class Transaction:
    def __init__(self, connection):
        self.connection = connection

    def commit(self):
        self.connection.commit()

    def rollback(self):
        self.connection.rollback()
