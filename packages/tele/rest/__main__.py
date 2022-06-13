from flask import Flask

app: Flask = Flask(__name__)

@app.route("/")
def hello():
    return "<h1>Hello</h1>"

if __name__ == '__main__':
    print("Start")