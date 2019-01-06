from flask import Flask, render_template, request, redirect,session
import random


app = Flask(__name__)
app.secret_key ='Nobreak'
# our index route will handle rendering our form
@app.route('/')
def index():
    print('\n\n')
    
    if 'guess' not in session:
        session['guess']=""
    return render_template("index.html", guess= session['guess'])


@app.route('/process',methods=['POST'])
def process():
    number = request.form['number']
    randomvalue = random.randrange(0, 101)
    if int(number)>randomvalue:
        session['guess'] = "Too high"
    if int(number)<randomvalue:
        session['guess'] ="you guessed low"
        
    if int(number)==randomvalue:
        session.clear()
        session['guess']= "guess right"    
    print(session)
    print (randomvalue)
    return redirect('/')
if __name__ =="__main__":
    app.run(debug=True)

