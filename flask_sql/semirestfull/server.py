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
    
    query ="select* from users"
    mysql =connectToMySQL('semi_user')
    allusers=mysql.query_db(query)
    print ('\n\n')
    # print(allusers)

    return render_template ('index.html',allusers=allusers)

@app.route('/addnewuser')
def addnewuser():
    return render_template('newuser.html')


@app.route('/new', methods =['POST'])
def new():
    print(request.form)
    data ={
        "name" :  request.form['name'],
        "email": request.form['email']
    }
    query ="insert into users(FullName,Email,Created_at) values(%(name)s,%(email)s,now());"
    mysql =connectToMySQL('semi_user')
    mysql.query_db(query,data)
  
    return redirect('/')

@app.route('/show/<int:id>')

def show(id):
    data = {
        "id": id
    }
    query = "select * from users where id = %(id)s"
    mysql =connectToMySQL('semi_user')
    matchinng_users= mysql.query_db(query,data)
    user=matchinng_users[0]
    print(user)

    return render_template('show.html', user = user)


@app.route('/edit/<int:id>')

def edit(id):
    data = {
        "id": id
    }
    query = "select * from users where id = %(id)s"
    mysql =connectToMySQL('semi_user')
    matchinng_users= mysql.query_db(query,data)
    user=matchinng_users[0]
    print(user)

    return render_template('edit.html', user = user)


@app.route('/update/<int:id>',methods=['POST'])
def update(id):

    data = {
        "id": id,
        "FullName":request.form['name'],
        "email": request.form['email']
    }
  

    query = " update users set FullName= %(FullName)s,Email = %(email)s where id = %(id)s"
    mysql =connectToMySQL('semi_user')
    mysql.query_db(query,data)
  
    return redirect('/')
@app.route('/delete/<int:id>')
def delete(id):
    data ={
        "id": id,
    }
    query ="delete from users where id = %(id)s"
    mysql =connectToMySQL('semi_user')
    mysql.query_db(query,data)
    return redirect('/')

if __name__=='__main__':
    app.run(debug=True)

