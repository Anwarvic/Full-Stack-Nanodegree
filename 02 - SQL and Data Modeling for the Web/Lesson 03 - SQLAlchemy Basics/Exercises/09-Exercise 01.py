from flask import Flask


app = Flask("app")

@app.route("/")
def index():
    return "Hello world"



if __name__ == "__main__":
    app.run(debug=True, port=3000)