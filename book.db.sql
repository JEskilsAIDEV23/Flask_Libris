BEGIN TRANSACTION;
CREATE TABLE IF NOT EXISTS "Review" (
	"id"	INTEGER,
	"book_id"	INTEGER NOT NULL,
	"review_name"	TEXT NOT NULL,
	"rating"	INTEGER NOT NULL,
	"review_text"	TEXT,
	PRIMARY KEY("id" AUTOINCREMENT)
);
CREATE TABLE IF NOT EXISTS "books" (
	"id"	TEXT NOT NULL UNIQUE,
	"book_id"	INTEGER NOT NULL,
	"book_title"	TEXT NOT NULL,
	"author_id"	TEXT NOT NULL,
	"author_name"	TEXT NOT NULL,
	"book_genre"	TEXT,
	"AuthLibrisSearch"	TEXT,
	"description"	TEXT,
	PRIMARY KEY("book_id" AUTOINCREMENT)
);
CREATE TABLE IF NOT EXISTS "OL_Books" (
	"OL_Aid"	TEXT,
	"OL_Wid"	TEXT,
	"OL_Title"	TEXT,
	"OL_Descr"	TEXT,
	"OL_link"	TEXT,
	PRIMARY KEY("OL_Wid")
);
CREATE TABLE IF NOT EXISTS "OL_isbn" (
	"OL_Wid"	TEXT,
	"OL_Bid"	TEXT,
	"OL_Aid"	TEXT,
	"OL_Title"	TEXT,
	"isbn_10"	TEXT,
	"isbn_13"	TEXT,
	"genre"	TEXT,
	PRIMARY KEY("OL_Bid")
);
CREATE TABLE IF NOT EXISTS "Authors" (
	"OL_id"	TEXT NOT NULL UNIQUE,
	"Author_name"	TEXT,
	"Author_id"	INTEGER,
	"Top_work"	TEXT,
	"wiki_bio"	TEXT,
	PRIMARY KEY("Author_id" AUTOINCREMENT)
);
CREATE VIEW [books_r] as 
SELECT books.id, Books.Book_id, Books.Book_Title, books.author_id, Books.Author_name, books.book_genre, books.AuthLibrisSearch,books.description, AVG(DISTINCT(Review.rating)) as 'Rating'
FROM books, Review
where books.Book_id = Review.Book_id
GROUP BY books.Book_id
order by Rating DESC;
CREATE VIEW [Top_Books] as 
SELECT books.id, Books.Book_id,  Books.Book_Title, Books.author_name, AVG(DISTINCT(Review.rating)) as 'Rating'
FROM books, Review
where books.Book_id = Review.Book_id
GROUP BY books.Book_id
order by Rating DESC;
CREATE VIEW [isbn13] as 
select OL_isbn.isbn_13 as "isbn", OL_isbn.OL_Bid, OL_isbn.OL_Title, OL_isbn.OL_Aid, OL_isbn.genre, OL_Books.OL_Descr
FROM OL_Books, OL_isbn
where OL_Books.OL_Wid = OL_isbn.OL_Wid and OL_isbn.isbn_13 Not Like "X";
CREATE VIEW [isbn10] as 
select OL_isbn.isbn_10 as "isbn", OL_isbn.OL_Bid, OL_isbn.OL_Title, OL_isbn.OL_Aid, OL_isbn.genre, OL_Books.OL_Descr
FROM OL_Books, OL_isbn
where OL_Books.OL_Wid = OL_isbn.OL_Wid and OL_isbn.isbn_10 Not Like "X";
CREATE VIEW [isbn13_add] as 
select distinct isbn13.isbn, isbn13.OL_Title, isbn13.OL_Aid, books.author_name, isbn13.genre, isbn13.OL_Descr
from books, isbn13
where books.author_id= isbn13.OL_Aid;
CREATE VIEW [isbn10_add] as 
select distinct isbn10.isbn, isbn10.OL_Title, isbn10.OL_Aid, books.author_name, isbn10.genre, isbn10.OL_Descr
from books, isbn10
where books.author_id= isbn10.OL_Aid;
COMMIT;
