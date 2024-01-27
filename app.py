from flask import Flask, request, render_template, redirect, flash, session
from flask_debugtoolbar import DebugToolbarExtension
from surveys import satisfaction_survey as survey

RESPONSES_KEY = "responses"

app = Flask(__name__)
app.config['SECRET_KEY'] ='secret'

debug = DebugToolbarExtension(app)

response = []

@app.route("/")
def show_survey_start():
    """Select a survey"""
    return render_template("survery_start.html", survery=survey)

@app.route("/begin", methods=['POST'])
def start_survey():
    """Clear the session of responses"""

    session[RESPONSES_KEY] = []

    return redirect("/questions/0")

@app.route("/answer", methods=["POST"])
def handle_question():
    """Save the responses and redirect to next question"""
    
    #get the response choice
    choice = request.form('answer')

    #add this response to the session
    responses = session[RESPONSES_KEY]
    responses.append(choice)
    session[RESPONSES_KEY] = responses

    if (len(responses) == len(survey.questions)):
        # They've answered all the questions! Thank them.
        return redirect("/complete")
    else:
        return redirect(f"/questions/{len(responses)}")
    
@app.route("/questions/<int:qid>")
def complete():
    "surcey complete. show completion page"
    return render_template("completion.html")