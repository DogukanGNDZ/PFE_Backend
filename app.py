
from flask import Flask
from src import create_app

app = create_app()

@app.route('/')
def index():
    return 'Hello, stranger!'

if __name__ == "__main__":
    app.run(host="127.0.0.1")