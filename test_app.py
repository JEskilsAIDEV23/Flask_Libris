from flask.testing import FlaskClient
import pytest
from app import app
import json
import requests
from unittest.mock import MagicMock, patch
from sqlite__db_OOP import *

@pytest.fixture
def client():
    with app.test_client() as client:
        yield client

"""def test_index(client: FlaskClient):
    response = client.get('/')
    assert response.status_code == 200
    assert b'Hello, World!' in response.data

def test_books(client: FlaskClient):
    response = client.get('/books')
    assert response.status_code == 200
    assert b'{"Author_id":"OL24950A","Author_name":' in response.data

def test_books_index(client: FlaskClient):
    response = client.get('/books/1')
    assert response.status_code == 200
    assert b'{"Author_id":"OL24950A","Author_name":' in response.data"""

"""def test_books_none_book(client: FlaskClient):
    response = client.get('/books/37')
    assert response.status_code == 200

    # Decode response.data if necessary and remove leading/trailing whitespace
    response_text = response.data.decode().strip()

    # Ensure the expected substring is present in the response data
    expected_message = 'Book_id 37 not found in database             Most likely due to deletion'
    assert expected_message in response_text"""

"""@pytest.fixture
def test_upd():
    data = {"Author_name" : "ErnieHacks","Description" : "PoorBert"}
    response = requests.put(f"http://localhost:5000/books/12", json=data)
    assert response.status_code == 200

def test_update_book(test_upd):
    pass  # This test function doesn't have any actual assertions as it relies on the fixture test_upd

@pytest.fixture
def test_add():
    data = {           
    "id" : "Banan666",
    "title" : "Bananerna",
    "author_id" : "Apan666",
    "author" : "Trazan",
    "genre" : "Cooking",
    "description" : "Kokbok"
}
    response = requests.post(f"http://localhost:5000/books", json=data)
    assert response.status_code == 200
def test_add_book(test_add):
    pass  # This test function doesn't have any actual assertions as it relies on the fixture test_upd


@pytest.fixture
def test_book_13_idx_upd():

    data = {"Genre" : "Sagor","Description" : "Du är inte riktigt klok Madicken"}
    response = requests.put(f"http://localhost:5000/books/13", json=data)
    assert response.status_code == 200

def test_update_book(test_book_13_idx_upd):
    pass  # This test function doesn't have any actual assertions as it relies on the fixture test_upd

def test_books_index13(client: FlaskClient):
    response = client.get('/books/13')
    assert response.status_code == 200
    expected ={"Author_id": "OL24950A","Author_name": "Lindgren, Astrid, 1907-2002","Book_Title": "Madicken","Book_id": 13,"Genre": "Sagor","isbn": "9129657865","Description": "Du är inte riktigt klok Madicken","rating": "No Current Reviews"}
    print(response.json)
    assert expected == response.json"""

"""@pytest.fixture
def test_del():
    response = requests.delete(f"http://localhost:5000/books/23")
    assert response.status_code == 200
    expected_message = 'Book: 23 successfully removed from Books'
    assert expected_message in response.text

def test_delete_book(test_del):
    pass  # This test function doesn't have any actual assertions as it relies on the fixture test_upd
"""
"""def test_books_search(client: FlaskClient):
    response = client.get('/books?author=Lindgren&title=madicken&genre=Sagor')
    assert response.status_code == 200
    expected ={
    "Madicken": {
        "Author_id": "OL24950A",
        "Author_name": "Lindgren, Astrid, 1907-2002",
        "Book_id": 13,
        "Book_title": "Madicken",
        "Description": "Du är inte riktigt klok Madicken",
        "Genre": "Sagor",
        "Rating": "No current reviews",
        "isbn": "9129657865"
    }
}
    assert expected == response.json"""

"""def test_books_top(client: FlaskClient):
    response = client.get('/books/top')
    assert response.status_code == 200
    content = list(response.json.values())

    n = 0
    for i in content:
        if "Rating" in i:
            n +=1
    assert n == 5"""

"""def test_reviews(client: FlaskClient):
    response = client.get('/reviews')
    assert response.status_code == 200
    content = list(response.json.values())

    n = 0
    for i in content:
        if n == 0:
            if "book_id" in i:
                if "book_title" in i:
                    if "rating" in i:
                        if "review" in i:
                            if "review_name" in i:
                                if "review_text" in i:
                                    n +=1
    assert n == 1

@pytest.fixture
def add_review():
    data = {
	"book_id":13,
	"rating":5,
	"review_name":"PyTortureTest",
	"review_text":"PyTest, Torture, PyTest WoW it Works"
    }
    response = requests.post(f"http://localhost:5000/reviews13", json=data)
    assert response.status_code == 200

def test_add_book(add_review):
    pass  # This test function doesn't have any actual assertions as it relies on the fixture"""
    

@pytest.fixture
def OL_api_response(requests_mock):
    author = "Johan+Eskils"
    # Define the URL of the mock API
    mock_url = f"https://openlibrary.org/search/authors.json?q={author}"
    json_response = {
  "numFound": 1,
  "start": 0,
  "numFoundExact": "true",
  "docs": [
    {
      "key": "OL690121XXXX",
      "text": ["Rather Smart and Lazy, than Dumb and Diligent"],
      "type": "author",
      "name": "J. Eskils",
      "alternate_names": ["Don Juan Eskils"],
      "birth_date": "21 Jan 1969",
      "top_work": "PyTest and PyTorture",
      "work_count": 1,
      "top_subjects": ['PythonicNightMares'],
      "_version_": 666
    },
  ]
}
    requests_mock.get(mock_url, json=json_response)


def test_send_request(OL_api_response):
    author = "Johan Eskils"
    author_url = '+'.join(author.split())
    response = requests.get(f"https://openlibrary.org/search/authors.json?q={author_url}")  
    assert response.status_code == 200
    print(response.text)
    with open('OL.json', 'w') as fd:
        fd.write(response.text)
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
    OL = OL_D["Key"][0]
    top_work = OL_D["top_work"]
    assert OL == "OL690121XXXX"
    assert top_work == "PyTest and PyTorture"
"""
@patch('sqlite3.connect')
def test_execute_query(mock_connect):
    mock_cursor = MagicMock()
    mock_connect.return_value.cursor.return_value = mock_cursor
    db = get_db_conn()
    
    # Mock a query execution
    books = db.execute_query("SELECT * FROM books_r")

    # Assert that the execute method was called with the correct query
    books = mock_cursor.execute.assert_called_once_with("SELECT * FROM books_r")
 
    # Mock database close method
    mock_cursor.close.return_value = None
    mock_connect.return_value.close.return_value = None
    db.db_close()

    # Assert that the close methods were called
    mock_cursor.close.assert_called_once()
    mock_connect.return_value.close.assert_called_once()
"""