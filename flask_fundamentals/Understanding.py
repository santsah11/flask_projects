from flask import Flask
app =Flask(__name__)

print(__name__)
@app.route('/')

def hello_world():
   
    print("\n this cool'\n")
   
    return 'Hello World'

@app.route('/dojo')
def dojo():
    return 'Its Dojo !'

@app.route('/say/<name>')
def say(name):
    return "Hello  " + name 


  
if __name__=="__main__":
    app.run(debug=True)