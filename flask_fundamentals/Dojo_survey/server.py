from flask import Flask, render_template , request,redirect,session

app =Flask(__name__)
print(__name__)

@app.route('/')
def surveyDojo():
    return render_template ("index.html")

@app.route("/result", methods=['post'])
def result():
    print("This is before form")
    print(request.form)
    print("This is after form!!!")

    return render_template("survey.html")  


if __name__=="__main__":

    app.run(debug=True)

