from flask import Flask,render_template,redirect,request,session,flash
import re
from mysqlconnection import connectToMySQL
from flask_bcrypt import Bcrypt
from datetime import datetime 
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
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
    mysql = connectToMySQL('nepal')
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
    mysql = connectToMySQL('nepal')
    user_id=mysql.query_db(query,data )
    print(user_id)
    session['user_id'] = user_id

    return redirect('/')
@app.route('/login', methods=['POST'])
def login():
    data = {
        "email" : request.form['email']
    }
    query = "SELECT * FROM users WHERE email = %(email)s"
    mysql = connectToMySQL('nepal')
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
    return redirect('/')

@app.route('/sign')
def sign():
    return render_template('sign.html')

@app.route('/admin')
def admin():
    return render_template('adminlogin.html')

@app.route('/adminlogin', methods=['POST'])
def adminlogin():
    data = {
        "email" : request.form['email']
    }
    query = "SELECT * FROM admins WHERE email = %(email)s"
    mysql = connectToMySQL('nepal')
    matching_email_users = mysql.query_db(query,data)
  
    if len(matching_email_users) == 0:
        flash("Invalid Credentials")
        print("bad email")
        return redirect('/admin')
    user = matching_email_users[0]
    print(user)
    if user['password'] != request.form['password']:
        flash("Invalid password")
        return redirect('/admin')
    session['user_name'] = user['first_name']
    session['user_id'] = user['id']
    return redirect('/adminpage')

@app.route('/adminpage')
def adminpage():
    query = "SELECT * FROM products;"
    mysql = connectToMySQL('nepal')
    products = mysql.query_db(query)
    return render_template('adminpage.html',products = products)

@app.route('/spice')
def spice():
    return render_template('spice.html')

@app.route('/collection/fetured')
def collectionfetured():
    query = "SELECT * FROM products;"
    mysql = connectToMySQL('nepal')
    products = mysql.query_db(query)
    return render_template('collectionfeature.html',products=products)


@app.route('/cart/add/<int:product_id>',methods=['POST'])
def cart(product_id):
    print(request.form)
    daata = request.form
    print(daata)
    data = {
        "product_id" :product_id
    }
    query = "SELECT * FROM products;"
    mysql = connectToMySQL('nepal')
    products = mysql.query_db(query)

    return redirect('/')

@app.route('/edit')
def edit():
    return render_template('edit.html')

@app.route('/add', methods = ['POST'])
def add():
    data ={
        "pname"   : request.form['pname'],
        "price"    : request.form['price'],
        "description"        : request.form['description'],
     }
    query = "insert into products (name,price,description,created_at, updated_at) VALUES (%(pname)s,%(price)s,%(description)s,now(),now())"
    mysql = connectToMySQL('nepal')
    product_id=mysql.query_db(query,data )
    print(product_id)
   
    return redirect('/edit')

if __name__=='__main__':
    app.run(debug=True)