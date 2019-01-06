from flask import Flask, render_template, request, redirect, session

from mysqlconnection import connectToMySQL
app = Flask(__name__)
@app.route('/')
def index():
    mysql = connectToMySQL('lead_gen_business')
    friends= mysql.query_db("SELECT client_id, first_name, last_name, email FROM clients;")
    
    return render_template('index.html', myfriends=friends)

if __name__ == "__main__":
    app.run(debug=True)