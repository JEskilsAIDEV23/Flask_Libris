from flask import request
import requests
from db_OOP import *
import json
#Rewritten for asynch
def libris_parse(data, author_url, OL):
    AuthLibrisSearch = author_url.replace('+',' ')
    if len(AuthLibrisSearch.split(' ')) > 1:
        auth_name_check = AuthLibrisSearch.split(' ')[1]
    if len(AuthLibrisSearch.split(' ')) <= 1:
        auth_name_check = AuthLibrisSearch.split(' ')[0]

    db = get_db_conn()

    n = 0
    for book in data:
        if "creator" in book:
            if isinstance(book["creator"], list):        
                author_name = book["creator"][0]                              
        if "creator" in book:
            author_name = book["creator"]
        if "creator" not in book:
            author_name = 'None'
            print(f'Non valid record Author-{n}')
        if "title" in book:
            book_title = book["title"]
        if "title" not in book:
            book_title = 'None'
            print(f'Non valid record Title-{n}')       
        if "isbn" in book:
            if isinstance(book["isbn"], list):
                id = book["isbn"][0]
            else:
                id = book["isbn"]
        if "isbn" not in book:
            id = 'None'
            print(f'Non valid record isbn-{n}')
        if "type" in book:
            try:
                if book["type"] == 'book' and id != 'None' and author_name != 'None':
                    if auth_name_check in author_name.split(','):
                        author_id = OL
                        book_genre = 'X'
                        #book = Books(id, book_title, author_id, author_name, book_genre)
                        query_add = 'INSERT INTO books (id, book_title, author_id, author_name, book_genre, "AuthLibrisSearch") VALUES \
                            (?, ?, ?, ?, ?, ?)'  
                        db.execute_query(query_add, (id, book_title, author_id, author_name, book_genre, 'Libris'))   
            except:
                print (f"DB-Error: (Book with {id} already in DB)")
        n += 1 

    db.db_close()
    return "Books added to database"    

class Author:
    def __init__(self, OL_id, author_name, top_work, wiki_bio):
        self.OL_id = OL_id.strip()
        self.author_name = author_name.strip()
        self.top_work = top_work
        self.wiki_bio = wiki_bio
        try:
            if self.author_name == "":
                raise ValueError ("AuthorName require a valid input")

            if self.OL_id == "":
                raise ValueError ("AuthorID require a valid input")
        except ValueError as e:
            print(f"Author will not be updated: {e}")
            return None
        db = get_db_conn()
        try:
            query_add = 'INSERT INTO Authors ("OL_id", "Author_name", "Top_work", wiki_bio) VALUES \
            (?, ?, ?, ?)'
            db.execute_query(query_add, (self.OL_id, self.author_name, self.top_work, self.wiki_bio))
        except:
            print(f"DB-Error, Author {OL_id}, {author_name} already in DB")
        db.db_close()

class Books(): 
    def __init__(self, id, book_title, author_id, author_name, book_genre, description):
        self.id = id.strip()
        self.book_title = book_title.strip()
        self.author_id = author_id
        self.author_name = author_name
        self.book_genre = book_genre.strip()
        self.description = description.strip()      

def parse_file(OL):
    db = get_db_conn()
    with open('OL3.json', 'r') as f:
        OL3_data = f.read()
        print(OL3_data)
    data = json.loads(OL3_data)
    books_OL = {}
    for book in data.get('entries', []):
        if "key" in book:
            key = book['key'].replace('/works/','')
            books_OL[key] = {}
            books_OL[key]['link'] = {}
            books_OL[key]['link'] = f"https://openlibrary.org/works/{key}.json"
        if "title" in book:
            books_OL[key]['book_title'] = {}
            book_title = book["title"]
            books_OL[key]['book_title'] = book_title
        if 'description' in book:
            books_OL[key]['description'] = {}
            description = book['description']
            books_OL[key]['description'] = description
        if 'description' not in book:
            books_OL[key]['description'] = {}
            books_OL[key]['description'] = 'Not availible'

    for i in books_OL.keys():
        try:  
            query_add = 'INSERT INTO "OL_Books" ("OL_Aid", "OL_Wid", "OL_Title", "OL_Descr", "OL_link") VALUES (?, ?, ?, ?, ?)'
            db.execute_query(query_add, (OL, i, books_OL[i]['book_title'], books_OL[i]['description'], books_OL[i]['link'] ))
        except:
            print (f"DB-Error: (Book {i} already in db)")   
    db.db_close()
    return books_OL

def parse_works(OL, books_OL, genre_dict):
    db = get_db_conn()
    for i in books_OL.keys():
        work_url = f'https://openlibrary.org/works/{i}/editions.json'
        response = requests.get(work_url)
        url_OLData4 = response.json()
        data = url_OLData4['entries']
        
        for book in data:
            isbn_10 = 'X'
            isbn_13 = 'X'
            subject = 'None'

            if 'isbn_10' in book:
                isbn_10 = book['isbn_10'][0]                  
            if 'isbn_13' in book:
                isbn_13 = book['isbn_13'][0]
            if "title" in book:
                title = book['title']
            if 'key' in book:
                key = book['key'].replace('/books/','')
            if 'subjects' in book:
                n = 0
                subjects = book['subjects']
                if len(subjects) > 1 and n <1:
                    for subject in subjects:
                        if subject in genre_dict.keys():
                            genre = subject
                            n+=1
            
            try:
            # print(key, OL, title, isbn_10, isbn_13+'\n')    
                query_add = 'INSERT INTO "OL_isbn" ("OL_Wid", "OL_Bid", "OL_Aid", "OL_Title", isbn_10, isbn_13, genre) VALUES \
                (?, ?, ?, ?, ?, ?, ?)'
            #  print(query_add, (key, OL, title, isbn_10, isbn_13 ))
                db.execute_query(query_add, (i, key, OL, title, isbn_10, isbn_13, genre )) 
            except:
                print (f"DB-Error (Book {key} already in DB)")   
    db.db_close()

def OL_book_isbn10():
    db = get_db_conn()
    query_isbn10 = "SELECT * FROM isbn10_add"
    isbn10 = db.GET_query(query_isbn10)
    db.db_close()

    for i in isbn10:
        id = i[0]
        book_title = i[1]
        author_id = i[2]
        author_name = i[3]
        book_genre = i[4]
        description = i[5]
        query_add = 'INSERT INTO books (id, book_title, author_id, author_name, book_genre, "AuthLibrisSearch",description) VALUES \
        (?, ?, ?, ?, ?, ?, ?)'
        try:
            db = get_db_conn()
            db.execute_query(query_add, (id, book_title, author_id, author_name, book_genre, 'OL-isbn10',description))
            db.db_close()
        except:
            print("Book already in database")
            db.db_close()

def OL_book_isbn13():
    db = get_db_conn()
    query_isbn13 = "SELECT * FROM isbn13_add"
    isbn13 = db.GET_query(query_isbn13)
    db.db_close()

    for i in isbn13:
        id = i[0]
        book_title = i[1]
        author_id = i[2]
        author_name = i[3]
        book_genre = i[4]
        description = i[5]
        query_add = 'INSERT INTO books (id, book_title, author_id, author_name, book_genre, "AuthLibrisSearch",description) VALUES \
        (?, ?, ?, ?, ?, ?, ?)'
        try:
            db = get_db_conn()
            db.execute_query(query_add, (id, book_title, author_id, author_name, book_genre, 'OL-isbn13',description))
            db.db_close()
        except:
            print("Book already in database")
            db.db_close()     