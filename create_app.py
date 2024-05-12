from flask import Flask
import sqlite3
from flask import Flask, request
from werkzeug.exceptions import abort
import requests
import json
from sqlite__db_OOP import *
from db_mock import *
from urllib.parse import unquote
from book_deco import *
from app import app

def create_app():
    # Create the Flask application instance
    test_app = Flask(__name__)

    # Configuration settings (adjust these based on your needs)
    app.config['SECRET_KEY'] = '@1dEvtwo3s' #AIDEV23 ;-P
    import functools

    return app

# Example usage:
if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)
