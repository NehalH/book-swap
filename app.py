from flask import Flask, render_template, request, redirect, url_for, session
from models import *
from sqlalchemy import desc

app = Flask(__name__, static_folder='templates/assets')
app.secret_key = 'your_secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:papaya@localhost:5432/bookswap'
db.init_app(app)

# Home-page (Logged-out)    //////////////////////////////////////////////////////////////////////////////
@app.route("/")
def index():
    book_count = Book.query.count()
    reader_count = Reader.query.count()
    location_count = Location.query.count()
    last_tuple = Exchange.query.order_by(desc(Exchange.exch_id)).first()
    exchange_count = last_tuple.exch_id

    return render_template('index.html', book_count=book_count, reader_count=reader_count, location_count=location_count,exchange_count=exchange_count)


# Signup    ////////////////////////////////////////////////////////////////////////////////////////////// 
@app.route("/signup", methods= ["GET","POST"])
def signup():
    return render_template('signupform.html')

@app.route('/signup-data', methods=['POST'])
def signup_data():
    fname = request.form['fname']           #First Name
    lname = request.form['lname']           #Last Name
    age = request.form['age']               #Age
    pincode = request.form['pincode']       #Pincode
    email = request.form['email']           #Email
    password = request.form['password']     #Password
    new_reader= Reader(fname=fname, lname=lname, age=age, pincode=pincode, email=email, password=password)
    location = Location.query.filter_by(pincode=pincode).first()
    if location is None:
        locname = request.form['locname']   #Location Name
        city = request.form['city']         #City
        state = request.form['state']       #State
        location = Location(pincode=pincode, locname=locname, city=city, state=state)
        db.session.add(location)
    db.session.add(new_reader)
    db.session.commit()
    return


# Login     //////////////////////////////////////////////////////////////////////////////////////////////
@app.route("/login", methods= ["GET","POST"])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        user = Reader.query.filter_by(email=email, password=password).first()
        if user:
            session['email'] = email
            session.permanent = True
            print('Login Successful')
            return redirect(url_for('userhome'))
        else:
            return 'Invalid Login Credentials' 
    else:
        return render_template('loginform.html')


# Logout   //////////////////////////////////////////////////////////////////////////////////////////////
@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')


# Home-page (Logged-in)    //////////////////////////////////////////////////////////////////////////////
@app.route('/user-home')
def userhome():
    if 'email' in session:
        email = session['email']
        session.permanent = True
        user = Reader.query.filter_by(email=email).first()
        if user:
            session['reader_id'] = user.reader_id
            session['pincode'] = user.pincode
        location = Location.query.filter_by(pincode=user.pincode).first()
        books = (Book.query.join(Location, Book.pincode == Location.pincode)
                 .filter(Location.city == location.city).all())
        book_authors = {}
        for book in books:
            book_authors[book.book_id] = Author.query.filter_by(book_id=book.book_id).all()
        return render_template('user-home.html', books=books, book_authors=book_authors, city=location.city, user= user)
    else:
        return redirect(url_for('login'))


# myBookShelf-page      //////////////////////////////////////////////////////////////////////////////
@app.route('/my-book-shelf')
def my_book_shelf():
    if 'email' in session:
        email = session['email']
        user = Reader.query.filter_by(email=email).first()
        book_shelf = Book_shelf.query.filter_by(reader_id=user.reader_id).first()
        books = Book.query.filter_by(shelf_id=book_shelf.shelf_id).all()
        book_authors = {}
        for book in books:
            book_authors[book.book_id] = Author.query.filter_by(book_id=book.book_id).all()
        return render_template('my-book-shelf.html', books=books, book_authors=book_authors, user=user)
    else:
        return redirect(url_for('login'))


# add-New-Book      //////////////////////////////////////////////////////////////////////////////
@app.route('/add-new-book')
def add_new_book():
    return render_template('add-new-book.html')

@app.route('/add-book', methods=['POST'])
def add_book():
    # Obtain form data
    bname = request.form['title']
    auth_name = request.form['author']
    pub_year = request.form['pub_year']
    category = request.form['category']

    email = session['email']
    reader = Reader.query.filter_by(email=email).first()
    reader_id = reader.reader_id
    pincode = reader.pincode

    # Obtain the reader's shelf_id from the database
    shelf = Book_shelf.query.filter_by(reader_id=reader_id).first()
    shelf_id = shelf.shelf_id

    # Create a new book
    new_book = Book(bname, pub_year, category, shelf_id, pincode)

    # Add the new book to the database
    db.session.add(new_book)
    db.session.commit()
    
    # Add the author information to the database
    new_author = Author(new_book.book_id, auth_name)
    db.session.add(new_author)
    db.session.commit()

    # Redirect the user back to the bookshelf page
    return redirect(url_for('my_bookshelf'))


# Edit-Book      //////////////////////////////////////////////////////////////////////////////
@app.route('/edit-book', methods=['POST'])
def edit_book():
    book_id = request.form['book_id']
    book = Book.query.filter_by(book_id=book_id).first()
    authors = Author.query.filter_by(book_id=book_id).first()

    return render_template('edit-book.html',book=book, authors=authors)

@app.route('/edit-data', methods=['POST'])
def edit_data():
    # Obtain form data
    book_id = request.form['book_id']
    bname = request.form['title']
    auth_name = request.form['author']
    pub_year = request.form['pub_year']
    category = request.form['category']

    # Get the book to be updated
    book = Book.query.filter_by(book_id=book_id).first()

    # Update the book information
    book.bname = bname
    book.pub_year = pub_year
    book.category = category
    db.session.commit()

    # Get the author to be updated
    author = Author.query.filter_by(book_id=book_id).first()
    
    # Update the author information
    author.auth_name = auth_name
    db.session.commit()

    # Redirect the user back to the bookshelf page
    return redirect(url_for('my_bookshelf'))


# Delete-Book      //////////////////////////////////////////////////////////////////////////////
@app.route('/delete_book', methods=['POST'])
def delete_book():
    book_id = request.form['book_id']
    book = Book.query.filter_by(book_id=book_id).first()

    if book:
        # Delete the book's authors from the Author table
        authors_to_delete = Author.query.filter_by(book_id=book_id).all()
        for author in authors_to_delete:
            db.session.delete(author)

        # Delete the book from the Book table
        db.session.delete(book)

        db.session.commit()
        return redirect(url_for('my_book_shelf'))
    else:
        print('Book not found!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!')
        return redirect(url_for('my_book_shelf'))


# Exchange-Book      //////////////////////////////////////////////////////////////////////////////
@app.route('/exchange-for/<book_id>')
def exchange_for(book_id):
    if 'email' in session:
        email = session['email']
        user = Reader.query.filter_by(email=email).first()
        book_1 = Book.query.filter_by(book_id=book_id).first()
        
        book_shelf = Book_shelf.query.filter_by(reader_id=user.reader_id).first()
        books = Book.query.filter_by(shelf_id=book_shelf.shelf_id).all()
        return render_template('exchange-for.html', books=books, user=user, book_id=book_id, book_1=book_1)
    else:
        return redirect(url_for('login'))

@app.route('/exchange-data', methods=['POST'])
def exchange_data():
    book_id_1 = request.form['book_id_1']
    book_id_2 = request.form['book_id_2']

    # Get the reader_id of the owners of book_id_1 and book_id_2 as Reader_1 and Reader_2
    book_shelf_1 = Book_shelf.query.join(Book, Book_shelf.shelf_id == Book.shelf_id).filter(Book.book_id == book_id_1).first()
    reader_1 = book_shelf_1.reader_id
    
    book_shelf_2 = Book_shelf.query.join(Book, Book_shelf.shelf_id == Book.shelf_id).filter(Book.book_id == book_id_2).first()
    reader_2 = book_shelf_2.reader_id

    # Insert the values into the Exchange table
    new_exchange = Exchange(reader_1=reader_1, reader_2=reader_2, book_1=book_id_1, book_2=book_id_2)
    db.session.add(new_exchange)
    db.session.commit()

    return redirect(url_for('userhome'))

# Exchange-Requests      //////////////////////////////////////////////////////////////////////////////
@app.route('/requests')
def requests():
    if 'email' in session:
        email = session['email']
        user = Reader.query.filter_by(email=email).first()
        reader_id_2=user.reader_id
        requests = Exchange.query.filter_by(reader_1=reader_id_2).all()
        
        reader_2_names = []
        book_2 = []
        book_1 = []
        for request in requests:
            reader_2 = Reader.query.filter_by(reader_id=request.reader_2).first()
            reader_2_names.append(reader_2.fname + " " + reader_2.lname)

            book_2_ele = Book.query.filter_by(book_id=request.book_2).first()
            print('000000000000000000000000000000000000000000000000000000000')
            print(book_2_ele.bname)
            book_2.append(book_2_ele.bname)
            book_1_ele = Book.query.filter_by(book_id=request.book_1).first()
            book_1.append(book_1_ele.bname)

        return render_template('requests.html', requests=requests, user=user, reader_2_names=reader_2_names, book_1=book_1, book_2=book_2)
    return redirect(url_for('login'))


@app.route('/accept/<exch_id>')
def accept(exch_id):
    exchange_request = Exchange.query.filter_by(exch_id=exch_id).first()

    reader_1_id = exchange_request.reader_1
    reader_2_id = exchange_request.reader_2

    shelf_1 = Book_shelf.query.filter_by(reader_id=reader_1_id).first
    shelf_2 = Book_shelf.query.filter_by(reader_id=reader_2_id).first

    book_1_id = exchange_request.book_1
    book_2_id = exchange_request.book_2
    book_1 = Book.query.filter_by(book_id=book_1_id).first()
    book_2 = Book.query.filter_by(book_id=book_2_id).first()

    temp = book_1.shelf_id
    book_1.shelf_id = book_2.shelf_id
    book_2.shelf_id = temp

    db.session.commit()

    db.session.delete(exchange_request)
    db.session.commit()

    return redirect(url_for('requests'))

@app.route('/reject/<exch_id>')
def reject(exch_id):
    exchange_request = Exchange.query.filter_by(exch_id=exch_id).first()
    db.session.delete(exchange_request)
    db.session.commit()
    return redirect(url_for('requests'))

# //////////////////////////////////////////////////////////////////////////////////////////////////////////////
if __name__ == '__main__':
    app.run(debug=True)
