from flask import Flask , render_template,session, redirect, request
import random
app= Flask(__name__)
app.secret_key ='thisIssecret'
#session = {
#     'gold': 0
# }

@app.route('/')
def index():
    # if t=user firstt time then give 
    if 'gold' not in session:
        session ['gold']= 0
        session['events']=[]

    return render_template("index.html")

@app.route('/process_money', methods =['POST'])
def process_money():
    
    if request.form['building']=='farm':
        gold_earned = random.randint(1,5)
        session['gold'] = session['gold'] + gold_earned
        print("got "  + str(gold_earned) + " from the farm")

    if request.form['building']=='cave':
        gold_earned = random.randint(10,20)
        session['gold'] = session['gold'] + gold_earned
        session['events'].append("got "  + str(gold_earned) + " from the cave")
    if request.form['building']=='casino':
        gold_earned = random.randint(10,20)
        session['gold'] = session['gold'] + gold_earned
        print("got "  + str(gold_earned) + " from the casino")
    if request.form['building']=='home':
        gold_earned = random.randint(-20,20)
        session['gold'] = session['gold'] + gold_earned
        if gold_earned >=0:
            print("won " +str(gold_earned) + " from the casino")
        else:
             print("lost " +str(gold_earned) + " from the casino")
        
        
    return redirect('/')

if __name__=="__main__":
    app.run(debug=True)