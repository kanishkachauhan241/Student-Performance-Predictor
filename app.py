from flask import Flask, render_template, request
import joblib
import pandas as pd

app = Flask(__name__)

# Load the trained model
model = joblib.load("student_model.pkl")


@app.route("/", methods=["GET", "POST"])
def home():

    prediction = None
    performance = None

    if request.method == "POST":

        study_hours = float(request.form["study_hours"])
        attendance = float(request.form["attendance"])
        assignments = float(request.form["assignments"])

        student = pd.DataFrame({
            "StudyHours": [study_hours],
            "Attendance": [attendance],
            "AssignmentsCompleted": [assignments]
        })

        marks = model.predict(student)[0]

        prediction = round(marks, 2)

        if marks >= 90:
            performance = "Excellent"
        elif marks >= 75:
            performance = "Very Good"
        elif marks >= 60:
            performance = "Good"
        elif marks >= 40:
            performance = "Average"
        else:
            performance = "Needs Improvement"

    return render_template(
        "index.html",
        prediction=prediction,
        performance=performance
    )


if __name__ == "__main__":
    app.run(debug=True)