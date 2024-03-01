import aiohttp
from flask import Flask, jsonify, request, render_template
import json
from cls_books import *
import requests
from db_OOP import *
from cls_books import *
from book_deco import *
from free_search_atg import *

#______THE SATANIC VERSES EDITION, ENHANCED TO MINE BOOKS_____"
#
# Learn the Rules Like a Pro, So You Can Break Them Like an Artist
# P.Picasso
#
# Hellre lat och smart än flitig och dum!
# Why spend hours on adding book data manually when you can mine it from the web.
# As I will do with data in the future and have done in my previous work life.
# Johan Eskils, AIDEV23S
#
# ENDPOINTS
#
# /author 
# External API Author search, that add the authors books to the local 
# database from libris.kb.se and uses Open Library author codes.
# The source of the book data is stored in the book table as tracking is
# essential for verifying data
#
# /books 
# search with /books?author=, /books?title=, /books?genre=
# does not require an exact match as author name varies with external sources
#
# /reviews 
#
# Templates for adding reviews and books, and updating book records are found
# after the main code.
#
# Database tables
# Authors : Store author data and updates with author-search and manual entries of books
# OL-Books : Store the Data Mining from an authors work as found in Open Library.
# OL-isbn : Store book editions derived from the Data mining of the authors work
# The two OL-tables provide enough information to create entries for the main books table
# books : Store the book data from the libris search, one drawback with libris is the lack
# of subject/genre information and thus genre is simplified and recorded as X in the 
# books table. 
# books_r: A generated SQL view of books with the addition of the calculated average ranking from reviews  
# Top_Books: A shorter column SQL-view than books_r
# isbn_13 and isbn_10: selective SQL-views that combine the results of the OL-tables
# isbn10 and isbn13: SQL-views that combine the author name from libris with the OL-tables
# to create a entry for the books table
# Review : Stores the reviews from users by book_id and a review_id 
#
# The database as the logic is built at the moment require more tables due to the mining 
# of book data from Open Library and Libris. Separate OL_books tables are used and combined with
# SQL-views to create book-data for the main books table.
# The Author table stores the results from the Author search such as wiki biography
# The book table author name is the name used in kb.libris.se and the author_id
# is the author-id used in open library
# A local database author_id and book_id are generated incrementally in the author and 
# books tables. isbn numbers are problematic as there are several editions of popular books, and 
# the mining as it is now have been simplified by using a limited number.
#
#__________________________________________________________

app = Flask(__name__)
app.config['SECRET_KEY'] = '@1dEvtwo3s'  # AIDEV23 ;-P

#____EXTERNAL API____Setting the Asynch____3 external API's are used
async def fetch_data(author_wiki, author_url):
    wiki_bio = 'NO BIO EXISTS'
    libris_data = None
    async with aiohttp.ClientSession() as session:
        async with session.get(f"https://en.wikipedia.org/api/rest_v1/page/summary/{author_wiki}", ssl=False) as wiki:
            if wiki.status == 200:
                data = await wiki.json()
                wiki_bio = data.get('extract', 'NO BIO EXISTS')

        async with session.get(f"http://libris.kb.se/xsearch?query={author_url}&format=json&n=50", ssl=False) as libris:
            if libris.status == 200:
                libris_data = await libris.json()
        await session.close()
    return wiki_bio, libris_data

async def libris(libris_data,author_url, OL): #BookData mining
    libris_parse(libris_data["xsearch"]['list'],author_url, OL)

async def fetch_OL(author_url): #author information from Open Library and initial entry for data mining
    session2 = aiohttp.ClientSession()
    async with session2.get(f"https://openlibrary.org/search/authors.json?q={author_url}", ssl=False) as OL:
        response_content = await OL.read()  # Read the entire response content
    with open('OL.json', 'wb') as fd:
        fd.write(response_content)
    await session2.close()

async def fetch_OL3(OL): #Grabs the author works and found entries are further used to mine book data
    session3 = aiohttp.ClientSession()
    async with session3.get(f'https://openlibrary.org/authors/{OL}/works.json', ssl=False) as OL_3:
        if OL_3.status == 200:
            OL3 = await OL_3.read()  # Read the entire response content
        with open('OL3.json', 'wb') as fd:
            fd.write(OL3)
        await session3.close()

async def parse_OL3(OL): #parse json file and then iterates through all entries functions are 
    books_OL = parse_file(OL) #located in cls_books
    return books_OL

async def isbn(): #
    OL_book_isbn10()
    OL_book_isbn13() 

@app.route('/author', methods=['GET'])
async def main():
    #initialize genre dict for assigning genres when book mining
    with open('genre.txt', 'r') as f:
        genre_dict = {}
        for i in f:
            i = i.replace('\n','')
            genre_dict[i] = i
    
    author = request.args.get('author')
    author_wiki = author.replace(' ', '_')
    author_url = '+'.join(author.split())
    try:
        wiki_bio, libris_data = await fetch_data(author_wiki, author_url)
        await fetch_OL(author_url)
        with open('OL.json', 'r') as f:
            OL_data = f.read() 
        data = json.loads(OL_data)
        OL_D = {}
        n = 0
        for auth in data.get('docs', []):
            OL_D["Author Name"] = auth.get('name')
            if n == 0:
                OL_D["Key"] = [auth.get('key')]
                OL_D[f"top_work"] = auth.get('top_work')
            n+=1

        OL = OL_D["Key"][0] #OL is the OL author-id and the key to mine book data
        top_work = OL_D["top_work"]
        summary = f"{OL}: {author} is most known for the work: {top_work}\n\nBiography:\n\nWikipedia\n{wiki_bio}"                     
        await libris(libris_data,author_url, OL) #not needed for the assignment
        await fetch_OL3(OL)       #Not needed for assignment
        books_OL = await parse_OL3(OL) #not needed for the assignment
        parse_works(OL, books_OL, genre_dict) #these steps take a lot of time #not needed for the assignment
        await isbn() #these steps take a lot of time #not needed for the assignment
        author = author_url.replace('+',' ')
        Author(OL, author, top_work, wiki_bio) 
        return summary
    except:
        return f"Author {author_wiki} don't exist or is not provided in the search"

#LOCAL Database ENTRYPOINTS
@app.route('/', methods=["GET"])
def hello_there():
    return render_template('index.html')
    
@app.route('/books', methods=["GET"])
def search_books():
    genre = request.args.get('genre')
    author = request.args.get('author')
    title = request.args.get('title')
    #___building the search logic___
    gta = ''
    if genre: 
        gta = gta+'g'
    if title:
        gta = gta+'t'
    if author:
        gta = gta+'a'

    if not genre and not author and not title:
        query ='SELECT * FROM books'
        db = get_db_conn()
        posts = db.GET_query(query)
        db.db_close()
        data = {}
        ret_data = []
        for i in range(len(posts)):
            db = get_db_conn()
            query_Book_r = "SELECT books_r.rating FROM books_r WHERE books_r.book_id = ?"
            reviews = db.GET_query(query_Book_r, (posts[i][1],) )
            db.db_close()
            if reviews == []:
                data = {
                'Book_title':posts[i][2],
                'Book_id' : posts[i][1], 
                'isbn' : posts[i][0],
                'Author_name' : posts[i][4],
                'Author_id' : posts[i][3],
                'Genre' : posts[i][5],
                'Description' : posts[i][7],
                'rating':'No current reviews'}   
            if reviews != []:
                data = {
                'Book_title':posts[i][2],
                'Book_id' : posts[i][1], 
                'isbn' : posts[i][0],
                'Author_name' : posts[i][4],
                'Author_id' : posts[i][3],
                'Genre' : posts[i][5],
                'Description' : posts[i][7],
                'rating': reviews[0][0]}
            ret_data.append(data)
        return jsonify(ret_data)
    #___calling the free_search functions that make queries
    if gta == 'g':
        posts =free_search_genre(genre)
    if gta == 't':
        posts = free_search_title(title)
    if gta == 'a':
        posts = free_search_author(author)
    if gta == 'ga' or gta == 'ag':
        posts = free_search_genre_n_author(genre, author)
    if gta == 'ta' or gta == 'at':
        posts = free_search_title_n_author(title, author)
    if gta == 'tg' or gta == 'gt':
        posts = free_search_genre_n_title(genre, title)
    if gta == 'gta':
        posts = free_search_genre_n_title_n_author(genre, title, author)             
    #re-written logic for books with reviews a query is made to the books_r
    #sql-view based on the book_id if a rating exist it is added to the result
    #slow approach but easier to track as the book_id has passed through the
    #free search and less risk for index-issues if reviews has not been deleted
    #from a database reset or not enough books has a review initially
    ret_data = []
    for i in range(len(posts)):
        db = get_db_conn()
        query_Book_r = "SELECT books_r.rating FROM books_r WHERE books_r.book_id = ?"
        reviews = db.GET_query(query_Book_r, (posts[i][1],) )
        db.db_close()
        if reviews == []:
            data = {
                'Book_title':posts[i][0],
                'Book_id' : posts[i][1], 
                'isbn' : posts[i][2],
                'Author_name' : posts[i][3],
                'Author_id' : posts[i][4],
                'Genre' : posts[i][5],
                'Description' : posts[i][6], #this index is dependant on the free search module
                'rating':'No current reviews'}   
        if reviews != []:
            data = {
                'Book_title':posts[i][0],
                'Book_id' : posts[i][1], 
                'isbn' : posts[i][2],
                'Author_name' : posts[i][3],
                'Author_id' : posts[i][4],
                'Genre' : posts[i][5],
                'Description' : posts[i][6], #this index is dependant on the free search module
                'rating' : reviews[0][0]}
        ret_data.append(data)
    return jsonify(ret_data)

@app.route('/books/<int:Book_id>', methods=["GET"])
def book_unique(Book_id):

     #same logic to check reviews for a single book
    query_Book_r = "SELECT books_r.rating FROM books_r WHERE Books_r.Book_id = ?"
    db = get_db_conn()
    review = db.GET_query(query_Book_r, (Book_id,) )
    db.db_close()
    if review == []:
        rev = "No Current Reviews"
    if review != []:
        rev = review[0][0]

    query_Book_id = "SELECT * FROM Books WHERE Books.Book_id = ?"
    db = get_db_conn()
    post = db.GET_query(query_Book_id, (Book_id,) )
    db.db_close()
    if post == []:
        return f"Book_id {Book_id} not found in database\
             Most likely due to deletion"
    if post != []:
        ret_data = []
        data = {'isbn' : post[0][0],
        'Book_id' : post[0][1],
        'Book_Title' :  post[0][2],
        'Author_id' : post[0][3],
        'Author_name' : post[0][4],
        'Genre' : post[0][5],
        'Description' : post[0][7],
        'rating' : rev}
    ret_data.append(data)
    return jsonify(ret_data)

@app.route('/books/top', methods=['GET'])
def top_books():
    #uses the simplified sql view Top-Books to find the 5 highest ranked books
    db = get_db_conn()
    query = f"SELECT * FROM TOP_books"
    books = db.GET_query(query)
    ret_data = []
    if len(books)<5:
        for i in range(len(books)):
            data = {"isbn":books[i][0], "Book_id":books[i][1], "Book_Title": books[i][2], 'Author_name':books[i][3], 'Rating':books[i][4]}
            ret_data.append(data)
    else:
        for i in range(5):
            data = {"isbn":books[i][0], 
                    "Book_id":books[i][1], 
                    "Book_Title": books[i][2], 
                    'Author_name':books[i][3], 
                    'Rating':books[i][4]}
            ret_data.append(data)
    db.db_close()
    return jsonify(ret_data)

@app.route('/books', methods=['POST'])
@print_body_books
def post_books():
    #logging of source for book data added and author added to author table if it does
    #not exist in database, the body is shown by the decorator in the console
    if request.method == 'POST':
        data = request.json
        if 'id' in data:
            OL_id = 1
            id = data['id']
        else:
            OL_id = 0
        if 'title' in data:
            book_title = data['title']
            BT = 1
        else:
            BT = 0
        if 'author' in data:
            author_name = data['author']
            AN = 1
        else:
            AN = 0
        if "author_id" in data:
            author_id = data['author_id']
            AI = 1
        else:
            AI = 0
        if "genre" in data:
            book_genre = data['genre']
            G = 1
        else:
            G = 0
        if "description" in data:
            description = data['description']
            D = 1
        else:
            D = 0
        if 'id' not in data or 'title' not in data or 'author' not in data or "author_id" not in data or "genre" not in data or "description" not in data:
            if (OL_id+BT+AN+AI+G+D) < 6:
                return f"\n Error: None valid and Missing data, Provided records with (1) are valid: id ({OL_id}), title ({BT}), author ({AN}), author_id ({AI}), genre ({G}), description ({D})"
        if (OL_id+BT+AN+AI+G+D) == 6:
            query_isbn = "SELECT * FROM books WHERE books.id = ?"
            db = get_db_conn()
            check = db.GET_query(query_isbn, (id,) )
            db.db_close()
            if check != []:
                return f"id/isbn {id} exist in DB"
            Author(author_id,author_name,'Manual Entry','Manual Entry')
            AuthLibrisSearch = "Manual Entry"
            try:
                if id.strip() == "":
                    raise ValueError ("id/isbn require a valid input not empty or blank")
                if book_title.strip() == "":
                    raise ValueError ("Book_title require a valid input not empty or blank")
                if book_genre.strip() == "":
                    raise ValueError ("Book_genre require a valid input not empty or blank")
                if author_id.strip() == "":
                    raise ValueError ("author_id require a valid input not empty or blank")
                if author_name.strip() == "":
                    raise ValueError ("author_name require a valid input not empty or blank")
                if description.strip() == "":
                    raise ValueError ("description require a valid input not empty or blank")
                else:
                    query_add = "INSERT INTO books (id, book_title, author_id, author_name, book_genre, AuthLibrisSearch, description) VALUES \
                        (?, ?, ?, ?, ?, ?, ?)"
                    db = get_db_conn()
                    db.execute_query(query_add, (id, book_title, author_id, author_name, book_genre, AuthLibrisSearch, description))
                    db.db_close()
                    return (f"{book_title} by {author_name} added successfully to the database")        
            except ValueError as e:
                return f"Value/DB-Error: {e}, Book isbn/id {id} with title {book_title} can't be added"
               
@app.route('/books/<int:Book_id>', methods=['DELETE'])
def delete(Book_id):
    #check if book exist in reviews and books before deletion
    db = get_db_conn()
    exists = ''
    query_Book_id = "SELECT * FROM Books WHERE Books.Book_id = ?"
    post_book = db.GET_query(query_Book_id, (Book_id,) )
    if post_book != []:
        exists += 'B'
    query_Review = "SELECT * FROM Review WHERE Review.Book_id = ?"
    post_review = db.GET_query(query_Review, (Book_id,) )
    if post_review != []:
        exists += 'R'
    if exists == '':
        return f"Book with Book_id {Book_id} don't exist in database"
    query_deleteB = f'DELETE FROM Books WHERE Book_id = ?'
    query_deleteR = f'DELETE FROM Review WHERE Book_id = ?'   
    if exists == 'BR':
        db.execute_query(query_deleteB, (Book_id,))
        db.execute_query(query_deleteR, (Book_id,))
        return f"Book: {Book_id} successfully removed from Books and Reviews"
    if exists == 'B':
        db.execute_query(query_deleteB, (Book_id,))
        return f"Book: {Book_id} successfully removed from Books"
    if exists == 'R':
        db.execute_query(query_deleteR, (Book_id,))
        return f"Book: {Book_id} successfully removed from Reviews" 
    db.db_close()

@app.route('/books/<int:Book_id>', methods=['PUT'])
@print_body_books
def edit(Book_id):
    #Check if book exist in database and if it exist allow edit
    #log update and store in book table source, AuthLibrisSearch (bad name but to many
    #dependencies to change and risk errors)
    if request.method == 'PUT':
        db = get_db_conn()
        query_Book_id = "SELECT * FROM Books WHERE Books.Book_id = ?"
        post_book = db.GET_query(query_Book_id, (Book_id,) )
        db.db_close()
        if post_book == []:
            return f"Book with id {Book_id} not found in database"
        else:
            #isbn (id) and book_id can't be edited to change a isbn the book must be
            #deleted and added again by search or manual entry. 
            data = request.json
            upd_sum = ''
            AuthLibrisSearch = "Manual Update"
            if 'Book_Title' in data:
                Book_Title = data['Book_Title'].strip()
                if Book_Title == "":
                    Book_Title = post_book[0][2]
                    BT = 0
                else:   
                    BT = 1
            else:
                 Book_Title = post_book[0][2]
                 BT = 0
            if 'Author_name' in data:
                Author_name = data['Author_name'].strip()
                if Author_name == "":
                    post_book[0][4]
                    AN = 0
                else:
                    AN = 1
            else:
                Author_name = post_book[0][4]
                AN = 0
            if "Author_id" in data:
                Author_id = data['Author_id'].strip()
                if Author_id== "":
                    post_book[0][3]
                    AI = 0
                else:
                    AI = 1
            else:
                Author_id = post_book[0][3]
                AI = 0
            if "Genre" in data:
                Genre = data['Genre'].strip()
                if Genre == "":
                    post_book[0][5]
                    G = 0
                else:
                    G = 1
            else:
                Genre = post_book[0][5]
                G = 0
            if "Description" in data:
                Description = data['Description'].strip()
                if Description == "":
                    D=0
                else:
                    D = 1
            else:
                Description = post_book[0][7]
                D = 0
            if 'Book_Title' not in data or 'Author_name' not in data or "Author_id" not in data or "Genre" not in data or "Description" not in data:
                if (BT+AN+AI+G+D) > 0:
                    upd_sum = f"\n Only the records with (1) are valid and will be updated: BookTitle ({BT}), AuthorName ({AN}), AuthorID ({AI}), Genre ({G}), Description ({D})"
            if (BT+AN+AI+G+D) > 0:
                upd_sum = f"\n Only the records with (1) are valid and will be updated: BookTitle ({BT}), AuthorName ({AN}), AuthorID ({AI}), Genre ({G}), Description ({D})"
            if (BT+AN+AI+G+D) == 0:
                return "Error: No valid input fields provided"
            if Author_name != "" and Author_id != "":
                Author(Author_id, Author_name, "from book_upd", "from book_upd")
            else:
                return "Error: Author_name and Author_id must not be null"     
            AuthLibrisSearch = 'Manual Update'
            #It refused to work with 100% safe code somehow
            query_update = f"UPDATE Books SET Book_Title ='{Book_Title}', Author_name='{Author_name}', \
                Author_id='{Author_id}', book_genre='{Genre}', AuthLibrisSearch= '{AuthLibrisSearch}',Description='{Description}' WHERE Book_id = ?"
            db = get_db_conn()
            db.execute_query(query_update, (Book_id,))
            db.db_close()
            return_string = f"Book with id {Book_id} Updated: "+upd_sum
            return return_string

###REVIEW ENTRY POINTS
#Check that book exist to allow addition of review 
#Review must contain book_id, rating and review_name, review_text is optional
        
@app.route('/reviews<int:book_id>', methods=['POST'])
@print_body_books
def add_book_review(*args,**kwargs):
    if request.method == 'POST':
        data = request.json
        data_l = len(data)
        if 'book_id' in data:
            Book_id = data['book_id']
        if 'book_id' not in data:
            return f"Invalid data or missing data"
    db = get_db_conn()
    query_Book_id = "SELECT * FROM books WHERE books.book_id = ?"
    post = db.GET_query(query_Book_id, (Book_id,) )
    if post == []:
        return f"Book_id {Book_id} not found in database\
             Most likely due to deletion"
    if data_l >=3: 
        if 'book_id' in data and 'review_name' in data and 'rating' in data:        
            Book_id = data['book_id']
            Customer_name = data['review_name'].strip()
            if Customer_name == '':
                return "review_name must not be blank or spaces"
            Customer_grade = data['rating']
            if "review_text" in data:
                Customer_text = data['review_text'].strip()
                if Customer_text == '':
                    Customer_text = 'No Text Review Submitted'
            if  "review_text" not in data:
                Customer_text = 'No Text Review Submitted'
            try:            
                if int(Customer_grade) < 1 or int(Customer_grade) > 5:
                    return 'Rating must be in the range 1-5'
            except:
                return "value error: rating is not an integer or null"
            query_add = "INSERT INTO review (book_id, review_name, rating, review_text) VALUES \
                (?, ?, ?, ?)"
            db.execute_query(query_add, (Book_id, Customer_name, Customer_grade, Customer_text))
            db.db_close()
            return f"Review added to Book_id: {Book_id}"
        else:
            return "Invalid data submitted"
    else:
        return f"Invalid data or missing data {data_l}/3 received"

@app.route('/reviews', methods=["GET"])
def all_reviews():
    db = get_db_conn()
    #SQL-madness is fun
    query = "SELECT Review.id, books.book_id, books.book_title, Review.review_name, \
        Review.rating, Review.review_text FROM Review, Books WHERE Books.Book_id = Review.Book_id"
    post = db.GET_query(query)
    db.db_close()
    data = {}
    ret_data = []
    for i in range(len(post)):
        data = {'review' : post[i][0],
        'book_id' : post[i][1],
        'book_title' : post[i][2],
        'review_name' : post[i][3],
        'rating' : post[i][4],
        'review_text' : post[i][5]}
        ret_data.append(data)
    return jsonify(ret_data)

@app.route('/reviews/<int:Book_id>', methods=["GET"])
def book_review(Book_id):
    db = get_db_conn()
    #___SQL___Easier to solve nested things with it
    query = f"SELECT Review.id, Books.Book_Title, books.author_name, Review.review_name, Review.rating,\
          Review.review_text FROM Review, Books WHERE books.book_id = Review.book_id and books.book_id = ?"
    post = db.GET_query(query, (Book_id,))
    if len(post) == 0:
        return "No Review exist for this book"		
    if len(post) >= 1:
        data = {}
        ret_data = []
        for i in range(len(post)):
            data = {'Rev_id' : post[i][0],
                    'Book_id' :  Book_id,
                    'Book_Title' : post[i][1],
                    'Author_name' : post[i][2],
                    'review_name' : post[i][3],
                    'rating' : post[i][4],
                    'review_text' : post[i][5]}
            ret_data.append(data)
        db.db_close()
        return jsonify(ret_data)

if __name__ == '__main__':
    app.run(debug=True)

"""
JSON FORMATS TO ADD AND UPDATE BOOKS
### To add a book follow this template where "id" is the isbn-number 
or any optional unique identifier

{           
    "id" : "1",
    "title" : "Bananerna",
    "author_id" : "1",
    "author" : "Trazan",
    "genre" : "Cooking",
    "description" : "Kokbok"
}

### To Update a book use this template to update the editable records
or select individual records. book_id and isbn number is not allowed
to update, to change a isbn number, the book must be deleted and added
manually to preserve a proper track record

{
	"Book_Title" : "876",
	"Author_name" : "Ernie",
	"Author_id" : "Bert",
	"Genre" : "Sesam",
	"Description" : "nu jävlar"
}

{
	"Author_name" : "Ernie",
	"Genre" : "Sesam",
	"Description" : "nu jävlar"
}

### To add review use these templates

{
	"book_id":876,
	"rating":4,
	"review_name":"Pythonian"
}

{
	"book_id":275,
	"rating":5,
	"review_name":"läskunnigPojke",
	"review_text":"Best I ever did not read"
}

"""