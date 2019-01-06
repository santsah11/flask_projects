from flask import Flask,render_template,redirect,request,session,flash
import re
from mysqlconnection import connectToMySQL
from flask_bcrypt import Bcrypt
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
app = Flask(__name__)
bcrypt = Bcrypt(app)
app.secret_key = "IAmGroot!"
@app.route('/')
def index():
    return render_template('index.html')   

@app.route('/register', methods = ['POST'])
def register():

    print(request.form)
    error = False
    if len(request.form['first_name'])<3:
        print('your name is too small')
        error =True
    if len(request.form['last_name'])<3:
        print('your last name too short')
        error =True
    if len(request.form['email'])<3:
        print('your emailis not valid')
        error =True
    if len(request.form['password']) <8:
        print('you password not good')
        error =True
    if request.form['password']!=request.form['c_password']:
        print('password did not match')
        error =True
    if not EMAIL_REGEX.match(request.form['email']):
        print('bolt not allowed')
        error =True
    if not request.form['last_name'].isalpha():
        print('number not allowed in the name')
        error =True
    if not request.form['first_name'].isalpha():
        print('number not allowed in the name')
        error =True
    data={
        "email": request.form['email']
    }
    query = "select * from users where email = %(email)s"
    mysql = connectToMySQL('wall_demo')
    match_email = mysql.query_db(query ,data)
    if len(match_email)>0:
        print("you already registered")
        return redirect('/')
    if error:
        return redirect('/')
    data ={
        "first_name": request.form['first_name'],
        "last_name" :request.form['first_name'],
        "email"     :request.form['email'],
        "password"  : bcrypt.generate_password_hash(request.form['password'])
    }
    query ="insert into users(first_name,last_name,email,password,created_at, updated_at) values(%(first_name)s,%(last_name)s,%(email)s,%(password)s,now(),now())"
    mysql = connectToMySQL('wall_demo')
    user_id=mysql.query_db(query,data )
    print(user_id)
    return redirect('/')

@app.route('/login',methods=['POST'])
def login():
    data ={
        "email": request.form['username'],
    }
    query = "select * from users where email = %(email)s"
    mysql = connectToMySQL('wall_demo')
    match_email = mysql.query_db(query ,data)
    if len(match_email) ==0:
        print ("no one has registered with this email")
        return redirect('/')
    user = match_email[0]
    if bcrypt.check_password_hash(user['password'], request.form['password']):
        session['user_id'] = user['id']
    return redirect('/wall')
@app.route('/wall', methods=['POST'])
    
   
    
if __name__ == "__main__":
    app.run(debug=True)