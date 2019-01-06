from flask import Flask , render_template
app= Flask(__name__)
# print(name)
@app.route('/')

def table():
    print("function is working ")

    users = (
   {'first_name' : 'Michael', 'last_name' : 'Choi'},
   {'first_name' : 'John', 'last_name' : 'Supsupin'},
   {'first_name' : 'Mark', 'last_name' : 'Guillen'},
   {'first_name' : 'KB', 'last_name' : 'Tonel'}
    )
    print ('\n\n')
    return render_template('Table.html', user = users)   
    
if __name__=="__main__":
    app.run(debug=True)
