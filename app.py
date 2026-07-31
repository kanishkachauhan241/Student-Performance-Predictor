from tracemalloc import start

from flask import Flask, render_template, request, send_file, flash
import joblib
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import os
import math
import io

from database import(
     get_connection,
     create_table,
     insert_prediction,
     get_predictions,
     search_predictions,
     get_predictions_paginated,
     count_predictions,
     get_statistics,
     get_performance_distribution
)

from datetime import datetime


total_predictions = 0
highest_marks = 0
average_marks = 0


app = Flask(__name__)
app.secret_key = "student_performance_secret"
create_table()

# Load the trained model
model = joblib.load("student_model.pkl")

  



@app.route("/", methods=["GET", "POST"])
def home():

    prediction = None
    performance = None
    error = None
    history = []
    total=request.args.get("page",1,type=int)
    per_page=5
    total_pages=1

    search = request.args.get("search", "")
    sort = request.args.get("sort", "")
    performance_filter = request.args.get("performance_filter", "")
    page = request.args.get("page", 1, type=int)
    per_page = 5


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

            insert_prediction(
                current_time,
                study_hours_float,
                attendance_float,
                assignments_float,
                prediction,
                performance
            ) 

            flash("Prediction saved successfully!", "success")   

    # Read history and generate dashboard
        history = get_predictions_paginated(
            page,
            per_page,
            search,
            sort,
            performance_filter
        )

        history_df = pd.DataFrame([dict(row) for row in history])

        if search:
            history_df = history_df[
                history_df.astype(str)
                .apply(lambda row: row.str.contains(search, case=False).any(), axis=1)
        ]


        if performance_filter:
            history_df = history_df[
                history_df["performance"] == performance_filter
            ]

        if sort == "newest":
            history_df = history_df.sort_values("timestamp", ascending=False)
        elif sort == "oldest":
            history_df = history_df.sort_values("timestamp", ascending=True)
        elif sort == "highest":
            history_df = history_df.sort_values("predicted_marks", ascending=False)
        elif sort == "lowest":
            history_df = history_df.sort_values("predicted_marks", ascending=True)

        total_predictions = count_predictions(
            search,
            performance_filter
        )
        stats=get_statistics()
        highest_marks = round(stats["highest"]or 0, 2)
        average_marks = round(stats["average"]or 0, 2)


        
        start = (page - 1) * per_page
        end = start + per_page

        recent = history_df.iloc[start:end]
        total_pages = max(1, math.ceil(len(history_df) / per_page))

        # Generate chart
        plt.plot(
            range(1, len(recent)+1),
            recent["predicted_marks"],
            marker="o",
            linewidth=2
        )

        plt.fill_between(
            range(1, len(recent)+1),
            recent["predicted_marks"],
            alpha=0.2
        )
        plt.title("Recent Predicted Marks")
        plt.xlabel("Recent Predictions")
        plt.ylabel("Marks")
        plt.grid(True)

        os.makedirs("static/images", exist_ok=True)

        plt.savefig("static/images/prediction_chart.png")
        plt.close()


        distribution = get_performance_distribution()
        labels = [row["performance"] for row in distribution]
        counts = [row["total"] for row in distribution]

        if labels:
            plt.figure(figsize=(6,4))
            plt.bar(labels, counts)
            plt.title("Performance Distribution")
            plt.xlabel("Performance")
            plt.ylabel("Students")
            plt.tight_layout()
            plt.savefig("static/images/performance_distribution.png")
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
            assignments=assignments,
            search=search,
            sort=sort,
            performance_filter=performance_filter,
            page=page,
            total_pages=total_pages
    )
@app.route("/clear_history",methods=["POST"])
def clear_history():
    conn=get_connection()
    conn.execute("DELETE FROM predictions")
    conn.commit()
    conn.close()
    if os.path.exists("static/images/prediction_chart.png"):
        os.remove("static/images/prediction_chart.png")

    flash("Prediction history cleared!","success")

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
        assignments="",
        page=1,
        total_pages=1
    )

@app.route("/download_history")
def download_history():
    history = get_predictions()
    if not history:
        return "No history available."

    df = pd.DataFrame([dict(row) for row in history])

    output = io.StringIO()

    df.to_csv(output, index=False)

    output.seek(0)

    return send_file(
        io.BytesIO(output.getvalue().encode()),
        mimetype="text/csv",
        as_attachment=True,
        download_name="prediction_history.csv"
    )


if __name__ == "__main__":
    app.run(debug=True)

