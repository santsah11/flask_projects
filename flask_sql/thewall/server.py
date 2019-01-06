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
@app.route('/register', methods =['POST'])
def registerr():
    error = False
    if len(request.form['first_name']) <3:
        flash("first Name mst be be more than 3 chsaracter")
    if len(request.form['last_name']) <3:
        flash("last anem canot be less than 3 ")
        error = True
    if len(request.form['password']) <8:
        flash('password must be 8 chracters')
        error = True
    if request.form['password']!=request.form['c_password']:
        flash("password should match")
        error= True
    if not request.form['first_name'].isalpha():
        flash("No number is alowed in name")
        error = True
    if not request.form['last_name'].isalpha():
        flash("No number is alowed in name")
        error = True
    if not EMAIL_REGEX.match(request.form['email']):
        flash('No bot emails allowed')
        error = True
    data = {
        "email" : request.form['email']
    }
    query = "SELECT * FROM users WHERE email = %(email)s"
    mysql = connectToMySQL('wall_demo')
    matching_email_users = mysql.query_db(query,data)
    if len(matching_email_users) > 0:
        flash("Identity theft is not a joke")
        error = True
    if error:
        return redirect('/')
    data ={
        "first_name"   : request.form['first_name'],
        "last_name"    : request.form['last_name'],
        "email"        : request.form['email'],
        "password"     : bcrypt.generate_password_hash(request.form['password'])
        }
    query = "insert into users (first_name,last_name,email,password,created_at, updated_at) values(%(first_name)s,%(last_name)s,%(email)s,%(password)s,now(),now())"
    mysql = connectToMySQL('wall_demo')
    user_id=mysql.query_db(query,data )
    print(user_id)
    session['user_id'] = user_id
    return redirect('/wall')

@app.route('/login', methods=['POST'])
def login():
    data = {
        "email" : request.form['email']
    }
    query = "SELECT * FROM users WHERE email = %(email)s"
    mysql = connectToMySQL('wall_demo')
    matching_email_users = mysql.query_db(query,data)

    if len(matching_email_users) == 0:
        flash("Invalid Credentials")
        print("bad email")
        
        return redirect('/')
    user = matching_email_users[0]
    if bcrypt.check_password_hash(user['password'], request.form['password']):
        session['user_id'] = user['id']
        return redirect('/wall')
    flash("Invalid Credentials")
    print("bad pw")
    return redirect('/')


@app.route ('/logout')
def logout():

    session.clear()
    return redirect('/')
   
@app.route('/wall')
def wall():
    if not 'user_id' in session:
        flash('out of here ')
        return redirect('/')
    #Logged user first name
    
    mysql = connectToMySQL('wall_demo')
    data={
        "user_id": session["user_id"]
    }
    query = "select first_name from users where id = %(user_id)s"
    the_user = mysql.query_db(query, data)
    print(the_user)
    #message for looged user
    mysql = connectToMySQL('wall_demo')
    data={
        "user_id": session["user_id"]
    }
    query = "select * from messages where rec_id = %(user_id)s"
    my_messages = mysql.query_db(query, data)
    print(my_messages)
    # message sent by  logged user 
    mysql = connectToMySQL('wall_demo')
    data={
        "user_id": session["user_id"]
    }
    query = "select * from messages where sender_id = %(user_id)s"
    sent_massages = mysql.query_db(query, data)
    
    #all user first name  and id
    mysql = connectToMySQL('wall_demo')
    query = "select id, first_name from users where id  != %(user_id)s"
    others_user = mysql.query_db(query, data)
   
    context = {
        "the_user" : the_user[0],
        "my_messages" : my_messages,
        "count_sent" : len(sent_massages),
        "others" :others_user
    }
    return render_template("wall.html", **context)
@app.route('/message/<int:rec_id>', methods=['POST'])
def add_message(rec_id):
    data = {
        "message" : request.form['message'],
        "sender_id" : session['user_id'],
        "receiver_id" : rec_id
    }
    query = "INSERT INTO messages (message, sender_id, rec_id, created_at, updated_at) VALUES (%(message)s, %(sender_id)s, %(receiver_id)s, NOW(), NOW());"
    mysql = connectToMySQL('wall_demo')
    mysql.query_db(query, data)
    return redirect('/wall')
@app.route('/delete/<int:del_id>')
def del_msg (del_id):
    data = {
        "del_id" : 'del_id'
    }
    query = "DELETE FROM messages WHERE id = %(del_id)s"
    mysql = connectToMySQL('wall_demo')
    mysql.query_db(query, data)
    return redirect('/wall')

if __name__ == "__main__":
    app.run(debug=True)