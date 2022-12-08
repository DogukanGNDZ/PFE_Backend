from flask import Flask
from src import create_app
from flask_cors import CORS

app = create_app()

cors = CORS(app, resources={r'/api/*': {"origins": "*"}})


@app.route('/')
def index():
    return 'Hello, stranger!'


if __name__ == "__main__":
    app.run(host="127.0.0.1")
