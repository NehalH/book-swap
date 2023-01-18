mesage = ''
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