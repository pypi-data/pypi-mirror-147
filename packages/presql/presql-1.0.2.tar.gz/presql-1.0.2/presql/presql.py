"""
    (c) 2022 Rodney Maniego Jr.
    Arkivist
"""

import psycopg2
import psycopg2.extras

class PreSQL():
    def __init__(self, uri=None, dbname=None, user=None, password=None, host=None, port=None, sslmode=None, autocommit=True):
        self._uri = uri
        self._dbname = dbname
        self._dbname = dbname
        self._user = user
        self._password = password
        self._host = host
        self._port = port
        self._sslmode = sslmode
        self._autocommit = autocommit
        self._connection = None
        self._cursor = None
 
    def __enter__(self):
        if not isinstance(self._uri, str):
            if not (isinstance(self._dbname, str) and isinstance(self._user, str) and isinstance(self._password, str)):
                assert False, "Database parameters must be in string format."
                return
        try:
            if isinstance(self._uri, str):
                if not isinstance(self._sslmode, str):
                    self._connection = psycopg2.connect(self._uri)
                else:
                   self._connection = psycopg2.connect(self._uri, sslmode=self._sslmode)
            elif isinstance(self._host, str) and isinstance(self._port, str):
                self._connection = psycopg2.connect(dbname=self._dbname,
                                                    user=self._user,
                                                    password=self._password,
                                                    host=self._host,
                                                    port=self._port)
            else:
                self._connection = psycopg2.connect(dbname=self._dbname,
                                                user=self._user,
                                                password=self._password)
            if self._connection is not None:
                self._cursor = self._connection.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        except:
            pass
        return self
    
    def set_client_encoding(self, encoding):
        if self._connection is not None:
            self._connection.set_client_encoding(encoding)
    
    def connected(self):
        return (self._connection is not None)
        
    def execute(self, query, values=None):
        if self._cursor is not None:
            if isinstance(query, str):
                try:
                    if isinstance(values, (list, set, tuple)):
                        self._cursor.execute(query, values)
                    else:
                        self._cursor.execute(query)
                    if isinstance(self._autocommit, bool) and bool(self._autocommit):
                        self._connection.commit()
                except:
                    self.rollback()
            return self._cursor
        
    def mogrify(self, query, values):
        if self._cursor is not None:
            if isinstance(query, str) and isinstance(values, (list, set, tuple)):
                try:
                    self._cursor.mogrify(query, values)
                    if isinstance(self._autocommit, bool) and bool(self._autocommit):
                        self._connection.commit()
                except:
                    self.rollback()
            return self._cursor
        
    def rollback(self):
        if self._cursor is not None:
            self._connection.rollback()
        
    def count(self, table, where=None):
        """ Get count of column based on the condition. """
        fconditions = f"WHERE {where}"
        if not isinstance(where, str):
            fconditions = ""
        cursor = self.execute(_cleaner(f"SELECT COUNT(*) FROM {table} {fconditions}"))
        if cursor is not None:
            row = cursor.fetchone()
            return int(row["count"])
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
        query = "SELECT"
        if isinstance(columns, str):
            query += f" {columns}"
        else:
            query += " *"
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
        cursor = self.execute(query)
        if cursor is not None:
            return cursor.fetchall()
        return []
        
    def insert(self, table, columns, values):
        """ Insert new table data. """
        if isinstance(columns, (list, set)):
            columns = ",".join(list(columns))
        if not isinstance(columns, str):
            print("PreSQL Warning: Columns only allow string or list objects only.")
            return
        data = []
        if isinstance(values, (list, set)):
            for value in values:
                data.append("(" + ",".join(list(columns)) + ")")
        if not isinstance(columns, str):
            print("PreSQL Warning: Values only allow string or list objects only.")
            return
        fdata = values
        if len(data):
            fdata = ", ".join(values)
        self.execute(_cleaner(f"INSERT INTO {table} ({columns}) VALUES {fdata}"))
        
    def update(self, table, columns, where=None):
        """ Insert new table data. """
        if isinstance(columns, (list, set)):
            columns = ",".join(list(columns))
        if not isinstance(columns, str):
            print("PreSQL Warning: Columns only allow string or list objects only.")
            return
        fdata = ""
        if isinstance(columns, dict):
            fcolumns = []
            for key, value in columns.items():
                fcolumns.append(f"{key}={value}")
            if len(fcolumns):
                fdata = ",".join(fcolumns)
        elif isinstance(columns, (list, set)):
            fdata = ",".join(list(columns))
        elif isinstance(columns, str):
            fdata = columns
        if not len(fdata):
            print("PreSQL Warning: Columns only allow string, list, or dictionary objects only.")
            return
        fconditions = ""
        if isinstance(where, str):
            fconditions = f"WHERE {where}"
        self.execute(_cleaner(f"UPDATE {table} SET {fdata} {fconditions}"))
        
    def delete(self, table, where=None):
        """ Get count of column based on the condition. """
        fconditions = f"WHERE {where}"
        if not isinstance(where, str):
            fconditions = ""
        self.execute(_cleaner(f"DELETE FROM {table} {fconditions}"))

    def __exit__(self, type, value, traceback):
        if self._cursor is not None:
            self._cursor.close()
        if self._connection is not None:
            self._connection.close()

def _cleaner(query):
    return query.strip().replace("  ", " ").replace(";", "") + ";"