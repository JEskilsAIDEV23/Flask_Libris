
import sqlite3
class get_db_conn:

    def __init__(self, db='Book.db'):
        self.conn = sqlite3.connect(db)
        #self.conn.row_factory = sqlite3.Row
        self.cursor = self.conn.cursor()

    def execute_query(self, query, parameters=None):
        try:
            if parameters:
                self.cursor.execute(query, parameters)
                self.conn.commit()
            else:
                self.cursor.execute(query)
                self.conn.commit()  # Commit changes to the database
            print('POST Query Executed successfully')
         #   return self.cursor.fetchall()
        except sqlite3.Error as e:
            #print(f"Database error: {e}")
            return []
        except Exception as e:
            #print(f"Error: {e}")
            return []

    def db_close(self):
        try:
            self.cursor.close()
            self.conn.close()
            print("Connection closed successfully.")
        except Exception as e:
            print(f"Error closing connection: {e}")

    def GET_query(self, query, parameters=None):
        try:
            if parameters:
                self.cursor.execute(query, parameters)
            else:
                self.cursor.execute(query)
            print('GET Query Executed successfully')
            return self.cursor.fetchall()
        except sqlite3.Error as e:
            print(f"Database error: {e}")
            return []
        except Exception as e:
            print(f"Error: {e}")
            return []