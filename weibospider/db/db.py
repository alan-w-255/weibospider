import psycopg2

class DB(object):
    conn = psycopg2.connect(
        database="mydb",
        user="alan",
        password="helloalan",
        host="localhost",
        port="5432"
    )

    def insert(self, values):
        pass

    def delete(self, values):
        pass


    def update(self, id, values):
        pass

    def closeDB(self):
        pass
    