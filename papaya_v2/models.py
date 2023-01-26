from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


# Reader        /////////////////////////////////////////////////////////////////////////
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


# Author        /////////////////////////////////////////////////////////////////////////
class Author(db.Model):
    book_id = db.Column(db.Integer, primary_key=True)
    auth_name = db.Column(db.String(30), nullable=False, primary_key=True)

    def __init__(self, book_id, auth_name):
        self.book_id = book_id
        self.auth_name = auth_name

    def __repr__(self):
        return '<Author %r>' % self.auth_name


# Book        /////////////////////////////////////////////////////////////////////////
class Book(db.Model):
    book_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    bname = db.Column(db.String(30), nullable=False)
    pub_year = db.Column(db.Integer)
    category = db.Column(db.String(50))
    shelf_id = db.Column(db.Integer)
    pincode = db.Column(db.Integer)

    def __init__(self, bname, publish_year, category, shelf_id, pincode):
        self.bname = bname
        self.pub_year = pub_year
        self.category = category
        self.shelf_id = shelf_id
        self.pincode = pincode

    def __repr__(self):
        return '<Book %r>' % self.bname


# Location        /////////////////////////////////////////////////////////////////////////
class Location(db.Model):
    pincode = db.Column(db.Integer, primary_key=True)
    locname = db.Column(db.String(20), nullable=False)
    city = db.Column(db.String(30), nullable=False)
    state = db.Column(db.String(30), nullable=True)

    def __init__(self, pincode, locname, city, state):
        self.pincode = pincode
        self.locname = locname
        self.city = city
        self.state = state

    def __repr__(self):
        return '<Location %r>' % self.city


# Exchange        /////////////////////////////////////////////////////////////////////////
class Exchange(db.Model):
    exch_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    reader_1 = db.Column(db.Integer, nullable=False)
    reader_2 = db.Column(db.Integer, nullable=False)
    book_1 = db.Column(db.Integer, nullable=False)
    book_2 = db.Column(db.Integer, nullable=False)

    def __init__(self, pincode, locname, city, state):
        self.pincode = pincode
        self.locname = locname
        self.city = city
        self.state = state

    def __repr__(self):
        return '<Exchange %r>' % self.exch_id


# Book_shelf        /////////////////////////////////////////////////////////////////////////
class Book_shelf(db.Model):
    shelf_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    reader_id = db.Column(db.Integer, nullable=False)

    def __init__(self, reader_id):
        self.reader_id = reader_id

    def __repr__(self):
        return '<Book_shelf %r>' % self.shelf_id