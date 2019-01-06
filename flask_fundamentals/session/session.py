from flask import Flask, render_template, request, redirect, session
app = Flask(__name__)
app.secret_key = 'ThisIsSecret' # Set a secret key for security purposes
@app.route('/')
def index():
    session['user']='Sant'
    
    return 'Index'
@app.route('/getsess')
def getsess():
    if 'user' in session:
        return session['user']
    return 'not logged in'    

if __name__=='__main__':
    app.run(debug=True)   