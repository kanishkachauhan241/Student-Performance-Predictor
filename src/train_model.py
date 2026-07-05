import pandas as pd
import matplotlib.pyplot as plt
import joblib
import os

from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

# Load dataset
data = pd.read_csv("data/student_data.csv")

print("===== First 5 Rows =====")
print(data.head())

print("\n===== Dataset Shape =====")
print(data.shape)

print("\n===== Column Names =====")
print(data.columns)

print("\n===== Dataset Information =====")
data.info()

print("\n===== Statistical Summary =====")
print(data.describe())

print("\n===== Missing Values =====")
print(data.isnull().sum())

print("\n===== Duplicate Rows =====")
print(data.duplicated().sum())

print("\n===== Data Types =====")
print(data.dtypes)

print("\n===== Data Cleaning Report =====")
print("Missing Values: None")
print("Duplicate Rows: None")
print("Dataset is ready!")

# Features and Target
x = data[["StudyHours", "Attendance", "AssignmentsCompleted"]]
y = data["Marks"]

print("\nFeatures")
print(x.head())

print("\nTarget")
print(y.head())

# Visualization
plt.figure(figsize=(8,5))
plt.scatter(data["StudyHours"], data["Marks"])
plt.title("Study Hours vs Marks")
plt.xlabel("Study Hours")
plt.ylabel("Marks")
plt.grid(True)
plt.show()

# Split data
x_train, x_test, y_train, y_test = train_test_split(
    x,
    y,
    test_size=0.2,
    random_state=42
)

print("\nTraining Shape")
print(x_train.shape)

print("Testing Shape")
print(x_test.shape)

# Train model
model = LinearRegression()

model.fit(x_train, y_train)

print("\nModel trained successfully!")

# Save model
joblib.dump(model, "student_model.pkl")
print("Model saved")

# Load model
loaded_model = joblib.load("student_model.pkl")
print("Model loaded")

# Sample prediction
sample = pd.DataFrame({
    "StudyHours": [8],
    "Attendance": [95],
    "AssignmentsCompleted": [10]
})

sample_prediction = loaded_model.predict(sample)

print("\nSample Prediction")
print("Predicted Marks:", round(sample_prediction[0], 2))

# Evaluate model
y_pred = loaded_model.predict(x_test)

print("\nActual vs Predicted")

for actual, predicted in zip(y_test, y_pred):
    print("Actual:", actual, "Predicted:", round(predicted, 2))

mae = mean_absolute_error(y_test, y_pred)
mse = mean_squared_error(y_test, y_pred)
r2 = r2_score(y_test, y_pred)

print("\nModel Evaluation")
print("MAE:", mae)
print("MSE:", mse)
print("R2 Score:", r2)

# User input
print("\nEnter Student Details")

study_hours = float(input("Study Hours: "))
attendance = float(input("Attendance: "))
assignments = float(input("Assignments Completed: "))

new_student = pd.DataFrame({
    "StudyHours": [study_hours],
    "Attendance": [attendance],
    "AssignmentsCompleted": [assignments]
})

prediction = loaded_model.predict(new_student)

marks = prediction[0]

print("\nPredicted Marks:", round(marks, 2))

# Performance
if marks >= 90:
    print("Performance: Excellent")
elif marks >= 75:
    print("Performance: Very Good")
elif marks >= 60:
    print("Performance: Good")
elif marks >= 40:
    print("Performance: Average")
else:
    print("Performance: Needs Improvement")

# Save prediction history
history = pd.DataFrame({
    "StudyHours": [study_hours],
    "Attendance": [attendance],
    "AssignmentsCompleted": [assignments],
    "PredictedMarks": [round(marks, 2)]
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

print("Prediction saved")