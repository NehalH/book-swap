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


# Home-page (Logged-in)    //////////////////////////////////////////////////////////////////////////////
@app.route('/user-home')
def userhome():
    if 'email' in session:
        email = session['email']
        session.permanent = True
        user = Reader.query.filter_by(email=email).first()
        location = Location.query.filter_by(pincode=user.pincode).first()
        books = Book.query.all()
        authors = Author.query.all()
        return render_template('user-home.html', books=books, authors=authors, city=location.city)
    else:
        return redirect(url_for('login'))


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


# Signup    ////////////////////////////////////////////////////////////////////////////////////////////// 
@app.route("/signup", methods= ["GET","POST"])
def signup():
    return render_template('signupform.html')

@app.route('/signup-data', methods=['POST'])
def signup_data():
    fname = request.form['fname']
    lname = request.form['lname']
    age = request.form['age']
    pincode = request.form['pincode']
    email = request.form['email']
    password = request.form['password']
    new_reader= Reader(fname=fname, lname=lname, age=age, pincode=pincode, email=email, password=password)
    db.session.add(new_reader)
    db.session.commit()
    return

if __name__ == '__main__':
    app.run(debug=True)
