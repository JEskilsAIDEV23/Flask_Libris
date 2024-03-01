Book database, extended version that collect books from KB_Libris when doing external author search from openlibrary.com
To tiresome to add books manually, asynched version and it includes all the features that was required for the assignment
The local database books can be searched with less restrictions than a perfect match of the author, title and genre
Genres are loaded from a file when initializing the app and thus the genres can be modified as openlibrary uses author topics
as genre and this app pick the first that matches. Author name is taken from libris database. json output have been rewritten
past hand in as they were nested dictionaires rather than in a flat list form and useful with pandas. Original app with nested 
json as output is also found as app.bak 
