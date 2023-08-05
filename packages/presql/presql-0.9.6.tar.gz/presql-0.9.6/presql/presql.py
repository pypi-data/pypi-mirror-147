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
        if isinstance(self.host, str) and isinstance(self.port, str):
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
        result = None
        if None not in (self.connection, self.cursor):
            if isinstance(query, str):
                if isinstance(values, (list, set, tuple)):
                    result = self.cursor.execute(query, values)
                else:
                    result = self.cursor.execute(query)
            self.connection.commit()
        return result
        
    def mogrify(self, query, values):
        result = None
        if None not in (self.connection, self.cursor):
            if isinstance(query, str) and isinstance(values, (list, set, tuple)):
                result = self.cursor.mogrify(query, values)
                self.connection.commit()
        return result
        
    def count(self, table, column=None, where=None):
        """ Get count of column based on the condition. """
        if not isinstance(column, str) or column is None:
            column = "*"
        conditions = ""
        if not isinstance(where, str) or where is None:
            conditions = f"WHERE {where}"
        rows = self.execute(f"SELECT COUNT(col) FROM table {conditions};")
        if rows is not None:
            for row in rows.fetchone():
                return int(row["usage"])
        return 0
    
    def select(self,
             table,
             columns=None,
             join=None,
             join_table=None,
             where=None,
             group=None,
             having=None,
             order=None,
             limit=None,
             offset=None):
        """ Formats SQL commands and returns appropriate iterable. """
        query = "SELECT *"
        if isinstance(columns, str):
            query.replace("*", columns)
        if isinstance(table, str):
            query += f" FROM {table}"
        if isinstance(join, str) and isinstance(join_table, str):
            query += f" {join} JOIN {join_table} ON"
        if isinstance(where, str):
            query += f" WHERE {where}"
        if isinstance(group, str):
            query += f" GROUP BY {group}"
        if isinstance(having, str):
            query += f" HAVING {having}"
        if isinstance(order, str):
            query += f" ORDER BY {order}"
        if isinstance(limit, int):
            query += f" LIMIT {limit}"
        if isinstance(offset, int):
            query += f" OFFSET {offset}"
        rows = self.execute(query+";")
        if rows is not None:
            return rows.fetchall()
        return ()

    def __exit__(self, type, value, traceback):
        if self.cursor is not None:
            self.cursor.close()
        if self.connection is not None:
            self.connection.close()