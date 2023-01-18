from flask import Flask, render_template, request, redirect, url_for
import psycopg2
import re

app = Flask(__name__, static_folder='templates/assets')

connection = psycopg2.connect(
    host="127.0.0.1",
    database="bookswap",
    user="postgres",
    password="papaya"
)

@app.route("/")
def index():
    return render_template('index.html')

@app.route("/login", methods= ["GET","POST"])
def login():
    print("=========================================")
    val2 = [j for j in request.form.values()]
    print(val2)
    return render_template('loginform.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index.html'))

@app.route("/signup", methods= ["GET","POST"])
def signup():
    print("=========================================")
    val2 = [j for j in request.form.values()]
    print(val2)
    
    # mesage = ''
    # if request.method == 'GET':
    #     return  render_template('signupform.html')
     
    # if request.method == 'POST' and 'fname' in request.form and 'lname' in request.form and 'age' in request.form and 'pincode' in request.form and 'email' in request.form and 'password' in request.form:
    #     fname = request.form['fname']
    #     lname = request.form['lname']
    #     age = request.form['age']
    #     pincode = request.form['pincode']
    #     email = request.form['email']
    #     password = request.form['password']

    #     cursor = connection.cursor()
    #     cursor.execute('SELECT * FROM Reader WHERE email = %s ', (email, ))
    #     account = cursor.fetchone()
    #     if account:
    #         flash('Account already exists!')
    #     elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
    #         flash('Invalid email address!')
    #     elif not email or not password:
    #         flash('Please fill out the form!')
    #     else:
    #         cursor.execute(' INSERT INTO Reader VALUES(NULL, %s , %s , %s , %s ,%s ,%s )',(fname,lname,age,pincode,email,password))
    #         mesage = 'You have successfully registered !'
    #     mysql.connection.commit()
    #     cursor.close()
    #     return  render_template('loginform.html', mesage = mesage)
    # elif request.method == 'POST':
    #     mesage = 'Please fill out the form !'
    # return  render_template('signupform.html', mesage = mesage)
    return render_template('signupform.html')

if __name__ == '__main__':
    app.run(debug=True)
