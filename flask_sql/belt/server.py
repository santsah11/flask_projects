from flask import Flask,render_template,redirect,request,session,flash
import re
from mysqlconnection import connectToMySQL
from flask_bcrypt import Bcrypt
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
from mysqlconnection import connectToMySQL
app = Flask(__name__)
bcrypt = Bcrypt(app)
app.secret_key = "IAmGroot!"

@app.route('/')
def index():
    return render_template ('index.html')

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
    elif len(request.form['lname']) <= 1:
        flash("Invalid Name!", 'entername')
        errors = True
    elif len(request.form['pw']) < 8:
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
    query = 'INSERT INTO users(fullname, alias, email, password,created_at,updated_at) VALUES(%(fna)s, %(lna)s, %(ema)s, %(pword)s,NOW(),NOW());'
    mysql = connectToMySQL('belt')
    user_id = mysql.query_db(query, data)
    print(user_id)
    session['user_id'] = user_id
    session['name'] = request.form['fname']

    return redirect("/")


@app.route('/login', methods = ['POST'])
def login():
    
    if len(request.form['logemail']) < 1:
        flash("Email cannot be blank!! ", "logemail")
        errors = True
        return redirect("/")
    elif not EMAIL_REGEX.match(request.form['logemail']):
        flash("Invalid Credentials!", 'logemail')
        errors = True
        return redirect("/")

    emvar = request.form['logemail']
    pwvar = request.form['logpw']
    print(emvar)
    print(pwvar)
    data = {
        'keyemail':request.form['logemail']
    }
    query = "SELECT * FROM users WHERE email = %(keyemail)s"
    mysql = connectToMySQL('belt')
    matching_email_users = mysql.query_db(query,data)
    print(matching_email_users)

    if len(matching_email_users) == 0:
        flash("Invalid Credentials...",'logemail' )
        return redirect('/')

    single_user = matching_email_users[0]
    if bcrypt.check_password_hash(single_user['password'], request.form['logpw']):

        session['name'] = single_user['fullname']
        session['user_id'] = single_user['id']

        return redirect('/books')       
    else:
        flash("password not match")
        return redirect("/")


@app.route('/books')
def success():

    query = 'select fullname from users join reviews on users.id= reviews.user_id where users.id= reviews.user_id;'
    mysql = connectToMySQL('belt')
    user_names=mysql.query_db(query)
    user=user_names[0]
    print(user)

    query = 'select * from books'
    mysql = connectToMySQL('belt')
    book_names=mysql.query_db(query)
    book_name=book_names[0]
    print(book_name)

    query = 'select * from reviews'
    mysql = connectToMySQL('belt')
    review=mysql.query_db(query)
    review=review[0]
    print(review)
    return render_template('books.html',book_name=book_name,review=review,user= user)

@app.route('/AddBookandreview')
def AddBookandreview():

   return  render_template ('addbook.html')

@app.route('/addbook',methods=['POST'])
def addbook():
    data = {
        "name": request.form['newauthor']
    }
    query = 'INSERT INTO authors(name,created_at,updated_at) VALUES(%(name)s,NOW(),NOW());'
    mysql = connectToMySQL('belt')
    author_id=mysql.query_db(query ,data)

    data = {
        "title": request.form['booktitle'],
        "author_id":author_id
    }
    query = "INSERT INTO books(title,created_at,updated_at,author_id) VALUES(%(title)s,NOW(),NOW(),%(author_id)s);"
    mysql = connectToMySQL('belt')
    book_id=mysql.query_db(query ,data)

    data = {
        "content": request.form['review'],
        "book_id" : book_id,
        "user_id": session['user_id'] 
    }
    query = "INSERT INTO reviews(content,created_at,updated_at,book_id,user_id) VALUES(%(content)s,NOW(),NOW(),%(book_id)s,%(user_id)s);"
    mysql = connectToMySQL('belt')
    mysql.query_db(query ,data)

    return redirect('/books')



if __name__=='__main__':
    app.run(debug=True)

