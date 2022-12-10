from flask import Flask
from src import create_app
from flask_cors import CORS
from dotenv import load_dotenv
import os

load_dotenv()
host = os.getenv("TEST")

app = create_app()

cors = CORS(app, resources={r'/api/*': {"origins": "*"}})


@app.route('/')
def index():
    print(host)
    return 'Hello, stranger!'+ host


if __name__ == "__main__":
    app.run()
