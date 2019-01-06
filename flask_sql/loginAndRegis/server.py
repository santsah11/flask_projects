from flask import Flask, render_template, request, redirect, session,flash
from mysqlconnection import connectToMySQL
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
from flask_bcrypt import Bcrypt
import re


app = Flask(__name__)
app.secrate_key = 'Issecrate'
becrypt = Bcrypt(app)
@app.route('/')
def index():
    
   
    return render_template('index.html')

@app.route('/register', methods = ['POST'])
def register():
    error = False
    if len(request.form[fname])<3:
        flash("Firast can not be less that 3 chars")
        error True
    if len(request.form[lname])<2:
        flash("can not be less than 2 chars")
        error True
    if len(request.form[email])<3:
        flash('emil is not good format')
        error True
    if len(request.form['password']) <8:
        flash('does not meet the standard')
        error True
    if request.form['email']!= requet.form['c_password']:

        flash('Not match th password')
        error True
    if not request.form['fname'].isalpha():
        flash('No  Numbers  in the name')
        error True
    if not EMAIL_REGEX.match(request.form['email']):
        flash('No  bolt email')
        error True
    data {
        "email": request.form['email']
    }
    query = "select * from users where email =%(email)s"
    mysql = connectToMySQL('wall_demo')
    matching_email_users = mysql.query_db(query,data)
    if len(matching_email_users)>0:
        flash('Identity theft Not a joke')
        error True
        if error:
            return('/')



if __name__ == "__main__":
    app.run(debug=True)
   