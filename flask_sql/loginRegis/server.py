from flask import Flask, render_template, redirect, request, session, flash
from mysqlconnection import connectToMySQL
import re
from flask_bcrypt import Bcrypt
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
app = Flask(__name__)
app.secret_key = "DarkSideoftheMoon!"
bcrypt = Bcrypt(app)

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/loginReg', methods = ["POST"])
def reserve():
    errors = False
    if len(request.form['email']) < 1:
        flash("Email cannot be blank!!! ", "email")
        errors = True
    elif not EMAIL_REGEX.match(request.form['email']):
        flash("Invalid Credentials!", 'email')
        errors = True
    elif len(request.form['fname']) < 1:
        flash("Name cannot be blank!", 'fname')
        errors = True
    elif len(request.form['lname']) <= 3:
        flash("Invalid Name!", 'entername')
        errors = True
    elif len(request.form['pw']) < 8 or len(request.form['pw']) > 15:
        flash("Password must be 8-15 char", 'pw')
        errors = True
    elif request.form['pw'] != request.form['confpw']:
        flash("Passwords must match!!",'confpw')
        errors = True 
    if errors == True:
        return redirect('/')

    data = {
        'fna':request.form['fname'],
        'lna':request.form['lname'],
        'ema':request.form['email'],
        'pword':bcrypt.generate_password_hash(request.form['pw'])
    }
    query = 'INSERT INTO regusers(fname, lname, email, pw) VALUES(%(fna)s, %(lna)s, %(ema)s, %(pword)s);'
    mysql = connectToMySQL('regandlogin')
    user_id = mysql.query_db(query, data)
    print(user_id)
    session['user_id'] = user_id
    session['name'] = request.form['fname']

    return redirect("/")

    


@app.route('/success')
def success():
    return render_template("/success.html")

@app.route('/login', methods = ['POST'])
def login():
    emvar = request.form['logemail']
    pwvar = request.form['logpw']
    data = {
        'keyemail':request.form['logemail']
    }
    if len(request.form['logemail']) < 1:
        flash("Email cannot be blank!! ", "logemail")
        errors = True
        return redirect("/")
    elif not EMAIL_REGEX.match(request.form['logemail']):
        flash("Invalid Credentials!", 'logemail')
        errors = True
        return redirect("/")
    query = "SELECT * FROM regusers WHERE email = %(keyemail)s"
    mysql = connectToMySQL('regandlogin')
    matching_email_users = mysql.query_db(query,data)
    if len(matching_email_users) == 0:
        flash("Invalid Credentials...",'logemail' )
        return redirect('/')
    single_user = matching_email_users[0]
    if bcrypt.check_password_hash(single_user['pw'], request.form['logpw']):
        session['name'] = single_user['fname']
        session['user_id'] = single_user['id']
        return redirect("/success")        
    else:
        return redirect("/")



if __name__ == '__main__':
    app.run(debug=True)
