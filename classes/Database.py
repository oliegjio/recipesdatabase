import sqlite3, os

class Database():
    """ Class providing database access.

    Can query data, and return it.
    """

    class __Database():

        def __init__(self, path):
            if not os.path.isfile(path):
                raise Exception("""Database does not exists in the given path!""")

            if not os.access(path, os.R_OK):
                raise Exception("""Cannot read the database!""")

            if not os.access(path, os.W_OK):
                raise Exception("""Cannot write to the database!""")

            self._connection = sqlite3.connect(path)
            self._cursor = self._connection.cursor()

        def query(self, query, sequence=None):
            """ Query the database.
            
            Takes a query. Replaces placeholders in query with values in sequence dictionary (if present). Executes query. Commits changes to the database.
            
            Arguments:
                query {str} -- Containing a query, may contain '?' placeholders.
                sequence {dict} -- Contains '?' placeholders' data. Defaults to None.
            """

            if sequence == None:
                self._cursor.execute(query)
            else:
                self._cursor.execute(query, sequence)
            self._connection.commit()

        def fetch_one(self):
            """ Iterate through data. Give next element of current data sequence.
            
            Returns:
                {None} -- Next element of data sequence, fetched from database with last query.
            """

            return self._cursor.fetchone()

        def fetch_all(self):
            """ Gives all elments in current data sequence as dictionary.
            
            Returns:
                {Dictionary} -- Contains all the data, fetched from last database call.
            """

            return self._cursor.fetchall()

    instance = None

    def __new__(cls):
        if Database.instance == None:
            Database.instance = Database.__Database('data.db')
        return Database.instance

    def __getattr__(self, name):
        return getattr(Database.instance, name)

    def __setattr__(self, name):
        return setattr(Database.instance, name)

