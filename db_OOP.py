import psycopg2
from configparser import ConfigParser

def load_config(filename='database.ini', section='postgresql'):
    parser = ConfigParser()
    parser.read(filename)
    # get section, default to postgresql
    config = {}
    if parser.has_section(section):
        params = parser.items(section)
        for param in params:
            config[param[0]] = param[1]
    else:
        raise Exception(f'Section {0} not found in the {1} file'.format(section, filename))

    return config

# if __name__ == '__main__':
#     config = load_config()
#     print(config)

def connect():
    """ Connect to the PostgreSQL database server """
    config = load_config()
    # print(config)

    try:
        # connecting to the PostgreSQL server
        with psycopg2.connect(**config) as conn:
            print('Connected to the PostgreSQL server.')
            return conn
    except (Exception. DatabaseError ) as error:
        print(error)

class get_db_conn:

    def __init__(self):
        self.conn = connect()
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
        except psycopg2.Error as e:
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
        except psycopg2.Error as e:
            print(f"Database error: {e}")
            return []
        except Exception as e:
            print(f"Error: {e}")
            return []
        
# query_Book_id = 'SELECT * FROM books_r WHERE CAST(book_id AS INTEGER) = %s'

# book_id = 3  # Example book ID
# db_conn = get_db_conn()
# result = db_conn.GET_query(query_Book_id, (book_id,))

# query_add = 'INSERT INTO books (id, book_title, author_id, author_name, book_genre, "AuthLibrisSearch", description) VALUES (%s, %s, %s, %s, %s, %s, %s)'
# db = get_db_conn()
# db.execute_query(query_add, ('OL98','Balla Trazan Apanson','OL23','Trazan','Cooking','Nope','Cooking with Gorillas'))
# db.db_close()

# query_books = 'SELECT * FROM books'
# db_conn = get_db_conn()
# result = db_conn.GET_query(query_books)
# for i in result:
#     print(i[2]+" Written By "+i[4])




