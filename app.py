from flask import Flask, render_template, request
import pickle

model = pickle.load(open("model.pkl","rb"))
vectorizer = pickle.load(open("vectorizer.pkl","rb"))

app = Flask(__name__)

def explain_code(code):

    if "for" in code or "while" in code:
        return "This code uses a loop to repeat instructions."

    if "def" in code:
        return "This code defines a function."

    if "class" in code:
        return "This code defines a class."

    if "print" in code or "console.log" in code:
        return "This code prints output to the console."

    if "if" in code:
        return "This code uses a conditional statement."

    return "Basic program structure detected."


def syntax_check(code):

    try:
        compile(code,"<string>","exec")
        return "No Syntax Errors Detected"
    except Exception as e:
        return str(e)


def code_statistics(code):

    lines = len(code.split("\n"))
    characters = len(code)
    words = len(code.split())

    loops = code.count("for") + code.count("while")
    functions = code.count("def")

    return {
        "lines":lines,
        "characters":characters,
        "words":words,
        "loops":loops,
        "functions":functions
    }


@app.route("/",methods=["GET","POST"])
def home():

    prediction=""
    explanation=""
    error=""
    stats=None
    message=""
    status=""
    code=""

    if request.method=="POST":

        code=request.form["code"].strip()
        action=request.form["action"]

        if action == "clear":
            code=""
        elif code == "":
            message="⚠ Please paste a code snippet before running analysis."
            status="warning"

        else:

            if action=="detect":

                vec=vectorizer.transform([code])
                prediction=model.predict(vec)[0]

            elif action=="explain":

                explanation=explain_code(code)

            elif action=="syntax":

                error=syntax_check(code)

            elif action=="stats":

                stats=code_statistics(code)

    return render_template(
        "index.html",
        prediction=prediction,
        explanation=explanation,
        error=error,
        stats=stats,
        message=message,
        status=status,
        code=code
    )
if __name__=="__main__":
    app.run(debug=True)