from flask import Flask , render_template
app= Flask(__name__)
@app.route('/')
def chechboard():
    print("function is working ")

    return render_template('checkboard.html')

if __name__=="__main__":
    app.run(debug=True)
