from flask import Flask, render_template
app =Flask(__name__)
print(__name__)

@app.route('/play')
def hello_world():

    return render_template ("index.html")

@app.route('/play/<x>')
def boxtimes(x):

    return render_template("morebox.html", times=int(x) )

@app.route('/play/<x>/<green>')
def boxcolor(x, green):

    return render_template("morebox.html", times=int(x),greeny=green )

if __name__=="__main__":
    app.run(debug=True)

