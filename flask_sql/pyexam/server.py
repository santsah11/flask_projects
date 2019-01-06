from flask import Flask,render_template,redirect,request,session,flash
import re
from mysqlconnection import connectToMySQL
from flask_bcrypt import Bcrypt
from datetime import datetime 
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
from mysqlconnection import connectToMySQL
app = Flask(__name__)
bcrypt = Bcrypt(app)
app.secret_key = "IAmGroot!"

@app.route('/')
def index():
   return render_template ('index.html')
@app.route('/register', methods =['POST'])
def registerr():
    error = False
    if len(request.form['fname']) <2:
        flash("first Name mst be be more than 2 chsaracter")
    if len(request.form['lname']) <2:
        flash("last name canot be less than 2 ")
        error = True
    if not EMAIL_REGEX.match(request.form['email']):
        flash("not bots email is allowed")
        error=True
    if len(request.form['password']) <8:
        flash('password must be 8 chracters')
        error = True
    if request.form['password']!=request.form['c_password']:
        flash("password should match")
        error= True
    if not request.form['fname'].isalpha():
        flash("No number is alowed in name")
        error = True
    if not request.form['lname'].isalpha():
        flash("No number is alowed in last name")
        error = True
    data = {
        "email" : request.form['email']
    }
    query = "SELECT * FROM users WHERE email = %(email)s"
    mysql = connectToMySQL('pyexam')
    matching_email_users = mysql.query_db(query,data)
    if len(matching_email_users) > 0:
        flash("Identity theft is not a joke")
        error = True
    if error:
        return redirect('/')
    data ={
        "first_name"   : request.form['fname'],
        "last_name"    : request.form['lname'],
        "email"        : request.form['email'],
        "password"     : bcrypt.generate_password_hash(request.form['password'])
        }
    query = "insert into users (first_name,last_name,email,password,created_at, updated_at) values(%(first_name)s,%(last_name)s,%(email)s,%(password)s,now(),now())"
    mysql = connectToMySQL('pyexam')
    user_id=mysql.query_db(query,data )
    session['user_id'] = user_id
    return redirect('/')
@app.route('/login', methods=['POST'])
def login():
    data = {
        "email" : request.form['email']
    }
    query = "SELECT * FROM users WHERE email = %(email)s"
    mysql = connectToMySQL('pyexam')
    matching_email_users = mysql.query_db(query,data)
    if len(matching_email_users) == 0:
        flash("Invalid Credentials")
        print("bad email")
        return redirect('/')
    user = matching_email_users[0]
    print(user)
    if bcrypt.check_password_hash(user['password'], request.form['password']):
        flash("Invalid password")
        return redirect('/')
    session['user_name'] = user['first_name']
    session['user_id'] = user['id']
    return redirect('/quotes')
@app.route('/quotes')
def quotes():
    if not 'user_id' in session:
        flash("Get out of here")
        return redirect('/')

    data ={
        "user_id": session['user_id']
    }
    query ="select  quotes.user_id, users.first_name,quote,quotes.id from users join quotes on users.id = quotes.user_id"
    mysql = connectToMySQL('pyexam')
    posted_by= mysql.query_db(query)
    return render_template('/quotes.html',posted_by=posted_by)
@app.route('/user/<int:user_id>')
def user(user_id):
    data ={
        "user_id": user_id
    }
    query ="select quotes.user_id, users.first_name,quote,quotes.id from users left join quotes on users.id = quotes.user_id where quotes.user_id = %(user_id)s;"
    mysql = connectToMySQL('pyexam')
    user_post= mysql.query_db(query, data)
    print(user_post)
    return render_template('user.html',user_post=user_post)
@app.route('/addqoute', methods=['POST'])
def add():
    data ={
        "author"   : request.form['author'],
        "quote"    : request.form['qoute'],
        "user_id"   : session['user_id']
        }
    if len(request.form['qoute']) < 1:
        flash("your quote can not be empty")
        return  redirect('/quotes')
    query = "insert into quotes (author,quote,created_at, updated_at,user_id) VALUES(%(author)s,%(quote)s,now(),now(),%(user_id)s)"
    mysql = connectToMySQL('pyexam')
    mysql.query_db(query,data )
    error= True
    return  redirect('/quotes')
@app.route('/edit/<int:user_id>')
def editmyaccount(user_id):
   return render_template ('edit.html')
@app.route('/update',methods=['POST'])
def update():
    if not 'user_id' in session:
        flash("Get out of here")
        return redirect('/')
    error = False
    if len(request.form['fname']) <2:
        flash("first Name mst be be more than 2 chsaracter")
    if len(request.form['lname']) <2:
        flash("last name canot be less than 2 ")
        error = True
    if not EMAIL_REGEX.match(request.form['email']):
        flash("not bots email is allowed")
        error=True
    data = {
        "user_id"  : session['user_id'],
        "first_name"   : request.form['fname'],
        "last_name"    : request.form['lname'],
        "email"        : request.form['email'],
    }
    query = "SELECT * FROM users WHERE email = %(email)s"
    mysql = connectToMySQL('pyexam')
    matching_email_users = mysql.query_db(query,data)
    if len(matching_email_users) > 0:
        flash("Identity theft is not a joke")
        error = True
    if error:
        return redirect('/quotes')
    query = "update users set first_name= %(first_name)s, last_name = %(last_name)s, email =%(email)s where users.id = %(user_id)s"
    mysql = connectToMySQL('pyexam')
    mysql.query_db(query, data)
    return redirect('/quotes') 
@app.route('/delete/<int:quote_id>')
def delete(quote_id):
    data={
        "quote_id":quote_id,
        "user_id": session['user_id']
    }
    query="delete from quotes where quotes.id = %(quote_id)s AND quotes.user_id = %(user_id)s"
    mysql =connectToMySQL('pyexam')
    mysql.query_db(query,data)
    return redirect('/quotes')
@app.route ('/logout')
def logout():
    session.clear()
    return redirect('/')
@app.route('/back')
def back():
    return redirect('/quotes')
if __name__=='__main__':
    app.run(debug=True)
