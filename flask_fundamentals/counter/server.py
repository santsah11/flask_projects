
from flask import Flask, render_template, request, redirect, session
app = Flask(__name__)
app.secret_key = 'ThisIsSecret'
#session {count:25}
#session[count]

@app.route('/')
def index():
    if 'count' not in session:
        session['count'] =0
    session['count'] +=1  

    print('\n\n')
    return render_template('index.html')

@app.route('/add', methods=['POST'])
def addtime():
    session['count'] +=2
    return redirect('/')

@app.route('/reset', methods = ['POST'])
def reset():
    session.clear()
    return redirect('/')
if __name__=="__main__":
    app.run(debug=True)     