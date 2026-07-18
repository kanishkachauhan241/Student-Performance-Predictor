from flask import Flask, render_template, request, send_file, flash
import joblib
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import os

from datetime import datetime


total_predictions = 0
highest_marks = 0
average_marks = 0


app = Flask(__name__)
app.secret_key = "student_performance_secret"

# Load the trained model
model = joblib.load("student_model.pkl")

  



@app.route("/", methods=["GET", "POST"])
def home():

    prediction = None
    performance = None
    error = None
    history = []

    study_hours = ""
    attendance = ""
    assignments = ""

    total_predictions = 0
    highest_marks = 0
    average_marks = 0

    if request.method == "POST":

        study_hours = request.form["study_hours"]
        attendance = request.form["attendance"]
        assignments = request.form["assignments"]

        study_hours_float = float(study_hours)
        attendance_float = float(attendance)
        assignments_float = float(assignments)

        # Input validation
        if study_hours_float < 0 or study_hours_float > 24:
            error = "Study hours must be between 0 and 24."

        elif attendance_float < 0 or attendance_float > 100:
            error = "Attendance must be between 0 and 100."

        elif assignments_float < 0 or assignments_float > 20:
            error = "Assignments must be between 0 and 20."

        if error is None:

            student = pd.DataFrame({
                "StudyHours": [study_hours_float],
                "Attendance": [attendance_float],
                "AssignmentsCompleted": [assignments_float]
            })

            marks = model.predict(student)[0]

            # Keep prediction between 0 and 100
            marks = max(0, min(marks, 100))

            prediction = round(marks, 2)

            # Performance label
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

            current_time = datetime.now().strftime("%d-%m-%Y %H:%M:%S")        

            # Save prediction
            new_prediction = pd.DataFrame({
                "Timestamp": [current_time],
                "StudyHours": [study_hours],
                "Attendance": [attendance],
                "AssignmentsCompleted": [assignments],
                "PredictedMarks": [prediction],
                "Performance": [performance],
            })

            if os.path.exists("prediction_history.csv"):
                new_prediction.to_csv(
                    "prediction_history.csv",
                    mode="a",
                    header=False,
                    index=False
                )
            else:
                new_prediction.to_csv(
                    "prediction_history.csv",
                    index=False
                )
            flash("Prediction saved successfully!", "success")    

    # Read history and generate dashboard
    if os.path.exists("prediction_history.csv"):

        history_df = pd.read_csv("prediction_history.csv")

        total_predictions = len(history_df)
        highest_marks = round(history_df["PredictedMarks"].max(), 2)
        average_marks = round(history_df["PredictedMarks"].mean(), 2)

        recent = history_df.tail(5)

        # Generate chart
        plt.plot(
            range(1, len(recent)+1),
            recent["PredictedMarks"],
            marker="o",
            linewidth=2
        )

        plt.fill_between(
            range(1, len(recent)+1),
            recent["PredictedMarks"],
            alpha=0.2
        )
        plt.title("Recent Predicted Marks")
        plt.xlabel("Recent Predictions")
        plt.ylabel("Marks")
        plt.grid(True)

        os.makedirs("static/images", exist_ok=True)

        plt.savefig("static/images/prediction_chart.png")
        plt.close()

        history = recent.to_dict(orient="records")

    return render_template(
          "index.html",
            prediction=prediction,
            performance=performance,
            error=error,
            history=history,
            total_predictions=total_predictions,
            highest_marks=highest_marks,
            average_marks=average_marks,
            study_hours=study_hours,
            attendance=attendance,
            assignments=assignments
    )
@app.route("/clear_history", methods=["POST"])
def clear_history():

    if os.path.exists("prediction_history.csv"):
        os.remove("prediction_history.csv")

    if os.path.exists("static/images/prediction_chart.png"):
        os.remove("static/images/prediction_chart.png")

    return render_template(
        "index.html",
        prediction=None,
        performance=None,
        error=None,
        history=[],
        total_predictions=0,
        highest_marks=0,
        average_marks=0,
        study_hours="",
        attendance="",
        assignments=""
    )

@app.route("/download_history")
def download_history():

    if os.path.exists("prediction_history.csv"):
        return send_file(
            "prediction_history.csv",
            as_attachment=True
        )

    return "No history available."


if __name__ == "__main__":
    app.run(debug=True)

