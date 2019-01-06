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
    mysql = connectToMySQL('beltExam')
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
    mysql = connectToMySQL('beltExam')
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
    mysql = connectToMySQL('beltexam')
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
    return redirect('/travels')

@app.route('/travels')
def travel():
    if not 'user_id' in session:
        flash("Get out of here")
        return redirect('/')
   #displaying the logged in user trips

    data ={
        "user_id": session['user_id']
    }
    query ="select * from trips where trips.user_id = %(user_id)s"
    mysql = connectToMySQL('beltExam')
    created_trips= mysql.query_db(query,data)
    # dispaying the joined trips 
    data ={
        "user_id": session['user_id']
    }
    query ="select * from trips join joined_trips on joined_trips.trip_id= trips.id  where joined_trips.user_id =%(user_id)s"
    mysql = connectToMySQL('beltExam')
    joined_trips = mysql.query_db(query,data)

    # dispalying ohter users trips 

    query ="select* from  trips where trips.user_id !=%(user_id)s"
    mysql = connectToMySQL('beltExam')
    other_users=mysql.query_db(query, data)
    return render_template("travels.html",created_trips=created_trips,other_users=other_users,joined_trips=joined_trips)

@app.route('/join/<int:other_trip_id>')
def join(other_trip_id):
    data ={
        "other_trip_id" : other_trip_id,
        "user_id" : session['user_id']
    }
    query ="insert into joined_trips(user_id,trip_id ) VALUES(%(user_id)s, %(other_trip_id)s)"
    mysql = connectToMySQL('beltExam')
    joined_trips=mysql.query_db(query, data)
    return redirect('/travels')

@app.route('/addtrip')
def addtrip():

    return render_template('addtrip.html')


@app.route('/process', methods=['POST'])
def process():
    error = False
    if len(request.form['des']) ==0:
        flash('can not be empty')
        error =True
    if len(request.form['descrip']) ==0:
        flash ('can not be empty')
        error =True
    if len(request.form['startDate']) > 0:
        start_date = datetime.strptime(request.form['startDate'], '%Y-%m-%d')        

        if start_date < datetime.today():
            flash('start date cannot be a past date')
            error = True
    else:
        flash('please enter start date')
        error = True

    if len(request.form['endDate']) > 0:
        end_date = datetime.strptime(request.form['endDate'], '%Y-%m-%d')        

        if end_date < start_date:
            flash('end date cannot be before start date')
            error = True
    if error: 
   
        return redirect('/addtrip')
       
    data = {
        "des" : request.form['des'],
        "travel_start": request.form['startDate'],
        "travel_end": request.form['endDate'],
        "plan" : request.form['descrip'],
        "user_id": session['user_id']
    }
    query = "insert into trips(destination,travel_start,travel_end,plan,created_at,updated_at,user_id) VALUES(%(des)s,%(travel_start)s,%(travel_end)s,%(plan)s,now(),now(),%(user_id)s)"
    mysql = connectToMySQL('beltExam')
    submitted_plan = mysql.query_db(query,data)
    return redirect('/travels')

@app.route('/delete/<int:id>')
def delete(id):
    data ={
        "id": id
    }
    query ="delete from trips where id = %(id)s "
    mysql = connectToMySQL('beltExam')
    mysql.query_db(query,data)

    return redirect('/travels')

@app.route('/cancel/<int:trip_id>')
def cancel(trip_id):
    data ={
        "trip_id": trip_id,
        "user_id" : session['user_id']
    }
    query ="delete from joined_trips where trip_id = %(trip_id)s AND joined_trips.user_id = %(user_id)s"
    mysql = connectToMySQL('beltExam')
    mysql.query_db(query,data)
   
    return redirect('/travels')

@app.route('/view/<int:id>')
def view(id):
    print(id)
    data={
        "id": id,
        "user_id":session['user_id']
    }
    query = "select * from trips join users on trips.user_id= users.id where trips.id =%(id)s ;"
    mysql = connectToMySQL('beltExam')
    viewresult=mysql.query_db(query ,data)
    #other joning the trip
    query ="select  first_name from users join joined_trips on joined_trips.user_id = users.id join trips on trips.id = joined_trips.trip_id where trips.id =%(id)s"
    mysql = connectToMySQL('beltExam')
    other_joining =mysql.query_db(query ,data)
    return render_template('view.html',viewresult=viewresult[0],other_joining=other_joining)



@app.route('/back')
def back():
    return redirect('/travels')

@app.route ('/logout')
def logout():
    
    session.clear()
    return redirect('/')
if __name__=='__main__':
    app.run(debug=True)


    