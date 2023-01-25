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

class Author(db.Model):
    book_id = db.Column(db.Integer, primary_key=True)
    auth_name = db.Column(db.String(30), nullable=False, primary_key=True)

    def __init__(self, book_id, auth_name):
        self.book_id = book_id
        self.auth_name = auth_name

    def __repr__(self):
        return '<Author %r>' % self.auth_name

class Book(db.Model):
    book_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    bname = db.Column(db.String(100), nullable=False)
    pub_year = db.Column(db.Integer)
    category = db.Column(db.String(50))

    def __init__(self, bname, publish_year, category):
        self.bname = bname
        self.pub_year = pub_year
        self.gencategoryre = category

    def __repr__(self):
        return '<Book %r>' % self.bname
