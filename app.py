from flask import Flask, render_template, request
import joblib
import pandas as pd

import os

app = Flask(__name__)

# Load the trained model
model = joblib.load("student_model.pkl")


@app.route("/", methods=["GET", "POST"])
def home():

    prediction =None
    performance =None
    error =None
    history=[]

    if request.method == "POST":

        study_hours = float(request.form["study_hours"])
        attendance = float(request.form["attendance"])
        assignments = float(request.form["assignments"])

        if study_hours < 0 or study_hours > 24:
            error = "Study hours must be between 0 and 24."

        elif attendance < 0 or attendance > 100:
            error = "Attendance must be between 0 and 100."

        elif assignments < 0 or assignments > 20:
            error = "Assignments must be between 0 and 20."

        if error is None:

            student = pd.DataFrame({
                "StudyHours": [study_hours],
                "Attendance": [attendance],
                "AssignmentsCompleted": [assignments]
            })

            marks = model.predict(student)[0]

            
            marks = max(0, min(marks, 100))
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

            history = pd.DataFrame({
                "StudyHours": [study_hours],
                "Attendance": [attendance],
                "AssignmentsCompleted": [assignments],
                "PredictedMarks": [prediction],
                "Performance": [performance]
            })

            if os.path.exists("prediction_history.csv"):
                history.to_csv(
                    "prediction_history.csv",
                    mode="a",
                    header=False,
                    index=False
                )
            else:
                history.to_csv(
                    "prediction_history.csv", 
                    index=False
                )


    if os.path.exists("prediction_history.csv"):
        history = pd.read_csv("prediction_history.csv")
        history = history.tail(5).to_dict(orient="records")



    return render_template(
        "index.html",
        prediction=prediction,
        performance=performance,
        error=error,
        history=history
    )

if __name__ == "__main__":
    app.run(debug=True)