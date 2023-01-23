from flask import Flask, render_template, request, redirect, url_for, session
from models import *

app = Flask(__name__, static_folder='templates/assets')
app.secret_key = 'your_secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:papaya@localhost:5432/bookswap'
db.init_app(app)

# Home-page (Logged-out)    //////////////////////////////////////////////////////////////////////////////
@app.route("/")
def index():
    return render_template('index.html')


# Home-page (Logged-in)    //////////////////////////////////////////////////////////////////////////////
@app.route('/user-home')
def userhome():
    books = Book.query.all()
    return render_template('user-home.html', books=books)


# Login     //////////////////////////////////////////////////////////////////////////////////////////////
@app.route("/login", methods= ["GET","POST"])
def login():    
    return render_template('loginform.html')


# Logout   //////////////////////////////////////////////////////////////////////////////////////////////
@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index.html'))


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
