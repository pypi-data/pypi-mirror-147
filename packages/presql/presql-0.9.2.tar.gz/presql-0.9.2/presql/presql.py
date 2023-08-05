"""
    (c) 2022 Rodney Maniego Jr.
    Arkivist
"""

import psycopg2


class PreSQL():
    def __init__(self, dbname=None, user=None, password=None, host=None, port=None):
        self.dbname = dbname
        self.user = user
        self.password = password
        self.host = host
        self.port = port
        self.connection = None
        self.cursor = None
 
    def __enter__(self):
        if not isinstance(self.dbname, str) and isinstance(self.user, str) and isinstance(self.password, str):
            assert False, "Database parameters mus be in string format."
        if not isinstance(self.host, str) and isinstance(self.port, str):
            self.connection = psycopg2.connect(dbname=self.dbname,
                                               user=self.user,
                                               password=self.password,
                                               host=self.host,
                                               port=self.port)
        else:
            self.connection = psycopg2.connect(dbname=self.dbname,
                                               user=self.user,
                                               password=self.password)
        if self.connection is not None:
            self.cursor = self.connection.cursor()
        return self
    
    def set_client_encoding(self, encoding):
        if self.connection is not None:
            self.connection.set_client_encoding(encoding)
        
    def execute(self, query, values=None):
        if None not in (self.connection, self.cursor):
            if isinstance(query, str):
                if isinstance(values, (list, set, tuple)):
                    self.cursor.execute(query, values)
                else:
                    self.cursor.execute(query)
            self.connection.commit()
        
    def mogrify(self, query, values):
        if None not in (self.connection, self.cursor):
            if isinstance(query, str) and isinstance(values, (list, set, tuple)):
                self.cursor.mogrify(query, values)
                self.connection.commit()

    def __exit__(self, type, value, traceback):
        if self.cursor is not None:
            self.cursor.close()
        if self.connection is not None:
            self.connection.close()