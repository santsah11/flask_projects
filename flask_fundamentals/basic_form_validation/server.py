from flask import Flask, render_template, redirect, request, session, flash
app = Flask(__name__)
app.secret_key = 'KeepItSecretKeepItSafe'
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/process', methods=['Post'])
def process():
  #do some validations here!
    if len(request.form['full_name']) < 1:
      print("please enter valid name")
    else:

        print("you are good to go")   
#fLASH KIND OF VALIDATION WE CAN DO ON THE CLIENT SIDE
     if len(request.form['name']) < 1:
        flash("Name cannot be empty!"copy) # just pass a string to the flash function
    else:
        flash(f"Success! Your name is {request.form['name']}.") # just pass a string to the flash function    

    return redirect('/')

if __name__=="__main__":
    app.run(debug=True)
