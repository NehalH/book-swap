from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Reader(db.Model):
    reader_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    fname = db.Column(db.String(20), nullable=False)
    lname = db.Column(db.String(20), nullable=False)
    age = db.Column(db.Integer)
    pincode = db.Column(db.Integer, nullable=False)
    email = db.Column(db.String(20), nullable=False, unique=True)
    password = db.Column(db.String(20), nullable=False)

    def __init__(self, fname, lname, age, pincode, email, password):
        self.fname = fname
        self.lname = lname
        self.age = age
        self.pincode = pincode
        self.email = email
        self.password = password

    def __repr__(self):
        return '<Reader %r>' % self.email


class Book(db.Model):
    book_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(100), nullable=False)
    author = db.Column(db.String(50), nullable=False)
    publish_year = db.Column(db.Integer)
    genre = db.Column(db.String(50))

    def __init__(self, title, author, publish_year, genre):
        self.title = title
        self.author = author
        self.publish_year = publish_year
        self.genre = genre

    def __repr__(self):
        return '<Book %r>' % self.title