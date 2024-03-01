from db_OOP import *
#Free search local database as author is picked from external source the author name might vary

def free_search_author(author):
    db = get_db_conn()
    query = f"SELECT DISTINCT(books.book_title), books.book_id, books.id, books.author_name, books.author_id, books.book_genre, books.description FROM books WHERE books.author_name LIKE ?"
    posts = db.GET_query(query, (f'%{author}%',))
    db.db_close()
    print(f'%{author}%')
    print(posts)
    return posts

def free_search_title(title):
    db = get_db_conn()
    query = f"SELECT DISTINCT(books.book_title), books.book_id, books.id, books.author_name, books.author_id, books.book_genre, books.description FROM books WHERE books.book_title LIKE ?"
    posts = db.GET_query(query, (f'%{title}%',))
    db.db_close()
    print(f'%{title}%')
    print(posts)
    return posts

def free_search_genre(genre):
    db = get_db_conn()
    query = f"SELECT DISTINCT(books.book_title), books.book_id, books.id, books.author_name, books.author_id, books.book_genre, books.description FROM books WHERE books.book_genre LIKE ?"
    posts = db.GET_query(query, (f'%{genre}%',))
    db.db_close()
    print(f'%{genre}%')
    print(posts)
    return posts

def free_search_title_n_author(title, author):
    db = get_db_conn()
    query = f"SELECT DISTINCT(books.book_title), books.book_id, books.id, books.author_name, books.author_id, books.book_genre, books.description FROM books WHERE books.book_title LIKE ?\
        AND books.author_name LIKE ?"
    posts = db.GET_query(query, (f'%{title}%',f'%{author}%'),)
    db.db_close()
    print(posts)
    return posts

def free_search_genre_n_author(genre, author):
    db = get_db_conn()
    query = f"SELECT DISTINCT(books.book_title), books.book_id, books.id, books.author_name, books.author_id, books.book_genre, books.description FROM books WHERE books.book_genre LIKE ?\
        AND books.author_name LIKE ?"
    posts = db.GET_query(query, (f'%{genre}%',f'%{author}%'),)
    db.db_close()
    print(posts)
    return posts

def free_search_genre_n_title(genre, title):
    db = get_db_conn()
    query = f"SELECT DISTINCT(books.book_title), books.book_id, books.id, books.author_name, books.author_id, books.book_genre, books.description FROM books WHERE books.book_genre LIKE ?\
        AND books.book_title LIKE ?"
    posts = db.GET_query(query, (f'%{genre}%',f'%{title}%'),)
    db.db_close()
    print(posts)
    return posts

def free_search_genre_n_title_n_author(genre, title, author):
    db = get_db_conn()
    query = f"SELECT DISTINCT(books.book_title), books.book_id, books.id, books.author_name, books.author_id, books.book_genre, books.description FROM books WHERE books.book_genre LIKE ?\
        AND books.book_title LIKE ? AND books.author_name LIKE ?"
    posts = db.GET_query(query, (f'%{genre}%',f'%{title}%',f'%{author}%'),)
    db.db_close()
    print(posts)
    return posts

#free_search_author('Tolkien')
#free_search_author('J. R. R.')
#free_search_title('Animal')
#free_search_title_n_author('Lord of','Tolkien')
#free_search_genre('Fiction')
#free_search_genre_n_title('Fiction','fula')
#free_search_genre_n_title_n_author('Fiction', 'Hob', 'Tolkien')

    #genre = request.args.get('genre')
    #author = request.args.get('author')
    #title = request.args.get('title')
    #author = author.replace('%20', ' ')
    #title = title.replace('%20', ' ')

def search_books(**kwargs):

    if len(kwargs) == 3:
        if 'genre' in kwargs and 'author' in kwargs and 'title' in kwargs:
            posts = free_search_genre_n_title_n_author(**kwargs)
        data = {}
        for i in range(len(posts)):
            data[posts[i][0]] = {}
            data[posts[i][0]]['Book_title'] = posts[i][0]
            data[posts[i][0]]['Book_id'] = posts[i][1]
            data[posts[i][0]]['isbn'] = posts[i][2]
            data[posts[i][0]]['Author_name'] = posts[i][2]
            data[posts[i][0]]['Author_id'] = posts[i][3]
            data[posts[i][0]]['Genre'] = posts[i][5]
            data[posts[i][0]]['Description'] = posts[i][6]
        return data
    if len(kwargs) == 2:
        if 'genre' in kwargs and 'author' in kwargs:
            posts = free_search_genre_n_author(**kwargs)
        if 'genre' in kwargs and 'title' in kwargs:
            posts = free_search_genre_n_title(**kwargs)
        if 'author' in kwargs and 'title' in kwargs:
            posts = free_search_title_n_author(**kwargs)
        data = {}
        for i in range(len(posts)):
            data[posts[i][0]] = {}
            data[posts[i][0]]['Book_title'] = posts[i][0]
            data[posts[i][0]]['Book_id'] = posts[i][1]
            data[posts[i][0]]['isbn'] = posts[i][2]
            data[posts[i][0]]['Author_name'] = posts[i][2]
            data[posts[i][0]]['Author_id'] = posts[i][3]
            data[posts[i][0]]['Genre'] = posts[i][5]
            data[posts[i][0]]['Description'] = posts[i][6]
        return data
    if len(kwargs) == 1:
        data = {}
        if 'genre' in kwargs:
            posts =free_search_genre(**kwargs)
        if 'author' in kwargs:
            posts = free_search_author(**kwargs)
        if 'title' in kwargs:
            posts = free_search_title(**kwargs)

        for i in range(len(posts)):
            data[posts[i][0]] = {}
            data[posts[i][0]]['Book_title'] = posts[i][0]
            data[posts[i][0]]['Book_id'] = posts[i][1]
            data[posts[i][0]]['isbn'] = posts[i][2]
            data[posts[i][0]]['Author_name'] = posts[i][2]
            data[posts[i][0]]['Author_id'] = posts[i][3]
            data[posts[i][0]]['Genre'] = posts[i][5]
            data[posts[i][0]]['Description'] = posts[i][6]
        return data
    
    if len(kwargs) == 0:
        if not kwargs['genre'] and not kwargs['author'] and not kwargs['title']:
            query ='SELECT * FROM books'
            db = get_db_conn()
            posts = db.GET_query(query)
            db.db_close()
            data = {}
            for i in range(len(posts)):
                data[posts[i][0]] = {}
                data[posts[i][0]]['Book_title'] = posts[i][0]
                data[posts[i][0]]['Book_id'] = posts[i][1]
                data[posts[i][0]]['isbn'] = posts[i][2]
                data[posts[i][0]]['Author_name'] = posts[i][2]
                data[posts[i][0]]['Author_id'] = posts[i][3]
                data[posts[i][0]]['Genre'] = posts[i][5]
                data[posts[i][0]]['Description'] = posts[i][6]
            return data

#search_books(title='1984')