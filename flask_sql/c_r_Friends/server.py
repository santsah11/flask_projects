from flask import Flask, render_template, request, redirect, session

from mysqlconnection import connectToMySQL
app = Flask(__name__)
@app.route('/')
def index():
    mysql = connectToMySQL('friendsdb')
    friends= mysql.query_db("SELECT first_name,last_name,occupation  FROM friends;")
    print(friends)
    return render_template('index.html', myfriends=friends)


@app.route('/addfriend', methods =['POST'])
def addfriend():
    mysql=connectToMySQL('friendsdb')
    print("databese connected")
    querry = "insert into friends ( first_name,last_name,occupation,created_at,updated_at) values (%(fname)s, %(lname)s, %(devloper)s ,now(),now())"
    data={"fname":request.form['first_name'],
            "lname":request.form['last_name'],
            "devloper": request.form['occupation']
         }
    mysql.query_db(querry, data)
    return redirect('/')


if __name__ == "__main__":
    app.run(debug=True)