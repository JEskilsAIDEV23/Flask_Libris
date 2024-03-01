Filer:

app.py : Main program, uppdelat I sektioner efter endpoints
		async definitioner
		/author 
		/books
		/reviews

		sist i app finns även beskrivningar av json-data för POST/PUT

book_deco.py : Innehåller definitionen av decorators

db_OOP.py : definition av läs/skriv funktionerna för databasen

cls_books.py : 	Innehåller funktioner mestadels för hämtning av bokdata från author search, klassen bok var/			är tänkt att hantera läs/skriv/check av bokdata, men logiken fungerade inte som den skulle.
			Innehåller också en funktion för att lägga till author data från sök i author tabellen. 					Komplexiteten i logiken med att hämta all information är inte helt klar.

free_search.atg.py :		Innehåller de kombinationer av sql-frågor som behövs för att kunna söka fritt på 						title, author and genre. Då hämtning av bokdata inte är så reglerad som vid 						manuell inmatning.

genre.txt : 	Innehåller subjects/genre för författare och används för att tilldela böcker en genre vid 				automatisk hämtning. Filen är skapad utifrån ett fåtal författares subjects. Filen går att 				redigera. genre.txt läses in som ett dictionary när appen startas.

book.db.sql :	skapar och initierar databasens tabeller och views

conftest.py, test_app.py, create_app.py : Innehåller pytest delen
test_protokoll.xlsx : de tester som gjorts

book.db : 			bokdatabasen som jag lagt till ett antal författare i 
generate.json :		funktion för att skapa och läsa in reviews till databasen

SQL-Tabeller
books, Review och Authors samt SQL-views Top_Books och books_r räcker för inlämningsuppgiften, isbn13, isbn10, isbn10_add, isbn13_add, OL_Books, OL_isbn är de tabeller som används för att lägga till böcker från Open Library. Libris saknar bra definitioner av genre men är utmärkt för att lägga till svenska böcker.

Med upptäckten av vad parquete och pyspark innebär så kommer nästa version hämta json, dumpa till parquet, använda pyspark-sql, plocka bokdata med sql-frågor och skicka resultatet till databasen.  

Johan Eskils, AIDEV23S