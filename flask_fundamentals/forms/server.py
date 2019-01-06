from flask import Flask, render_template, request, redirect,session

app = Flask(__name__)
app.secret_key ='Nobreak'
# our index route will handle rendering our form
@app.route('/')
def index():
    print('\n\n')
    return render_template("index.html")
# this route will handle our form submission
# notice how we defined which HTTP methods are allowed by this route


@app.route('/users', methods=['POST'])
def create_user():
    print("Got Post Info")
    # we'll talk about the following two lines after we learn a little more about forms
    session['name'] =  request.form['fullname'] # this how we can access the data from the form
    session['email'] = request.form['email']
    session['password'] = request.form['password']
    session.clear()
    # redirects back to the '/' route
    return redirect('/show')    

@app.route('/show')
def show_user():
        print('\n this new line \n')
        return render_template("user.html") # we can put in the render page or directly in the html,name= session['name'],email = session['email']

  
if __name__=="__main__":
    app.run(debug=True) 
