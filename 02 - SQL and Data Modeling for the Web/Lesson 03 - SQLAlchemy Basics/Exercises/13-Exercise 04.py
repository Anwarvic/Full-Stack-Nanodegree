from flask import Flask
from flask_sqlalchemy import SQLAlchemy


app = Flask("app")
app.config['SQLALCHEMY_DATABASE_URI'] = \
		'postgresql://student@localhost:5432/example'


db = SQLAlchemy(app)


class Person(db.Model):
    __tablename__ = 'persons'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(), nullable=False)


db.create_all()


@app.route('/')
def index():
    person = Person.query.first()
    return 'Hello ' + person.name


if __name__ == "__main__":
    app.run(debug=True)