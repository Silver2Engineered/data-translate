"""
Instructions to run:
    - [OPTIONAL] make and use a python venv with `python -m venv [venv name]` and `. [venv name]/bin/activate/`
    - `pip install flask`
    - `python app.py`
"""

from flask import Flask

app = Flask(__name__)

@app.route('/')
def hello_world():
    return "<p>Flask works!</p>"

if __name__ == "__main__":
    app.run()
    