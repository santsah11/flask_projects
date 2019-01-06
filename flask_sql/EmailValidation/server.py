from flask import Flask, render_template, request, redirect, session,flash
from flask_bcrypt import Bcrypt    
from mysqlconnection import connectToMySQL
import re
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
app = Flask(__name__)
bcrypt = Bcrypt(app)
app.secret_key = 'super secret key'
@app.route('/')
def index():
    return render_template('index.html')

        

@app.route('/process', methods=['POST'])
def process():
    isError = False #that means no error at this context
    if len(request.form['email'])==0:
        flash("provide the valid email")
        isError = True
    elif not EMAIL_REGEX.match(request.form['email']):
        flash("Invalid Email Address!", 'email')
        isError = True
    if isError:
        flash("there were errors")
    return redirect("/")
        
    mysql = connectToMySQL('User_emails')
    result=mysql.query_db('select * from emails')
    print(result)
    data ={"email":request.form['email']}
    query = "SELECT email FROM emails WHERE email_address = %(email)s" 
    emails = mysql.query_db(query, data)
    print(emails)
    session['email'] = emails[0]
    return redirect('/success' )


@app.route('/success')
def success():
    print(session)
    return render_template('success.html')
# function for success
# render the page
    
if __name__ == "__main__":
    app.run(debug=True)  
    