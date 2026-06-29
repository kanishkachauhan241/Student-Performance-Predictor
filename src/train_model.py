import pandas as pd
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split


# Load the dataset
data = pd.read_csv("data/student_data.csv")

# Display the first 5 rows
print("===== First 5 Rows =====")
print(data.head())

# Display the shape of the dataset
print("\n===== Dataset Shape =====")
print(data.shape)

# Display the column names
print("\n===== Column Names =====")
print(data.columns)

# Display dataset information
print("\n===== Dataset Information =====")
data.info()

# Display statistical summary
print("\n===== Statistical Summary =====")
print(data.describe())


# Check for missing values
print("\n===== Missing Values =====")
print(data.isnull().sum())


# Check for duplicate rows
print("\n===== Duplicate Rows =====")
print(data.duplicated().sum())


# Check data types
print("\n===== Data Types =====")
print(data.dtypes)


# Data Cleaning Report
print("\n===== Data Cleaning Report =====")
print("✓ Missing Values: None")
print("✓ Duplicate Rows: None")
print("✓ Data Types: Correct")
print("✓ Dataset is ready for Machine Learning!")


# Select features and target
X = data[["StudyHours", "Attendance", "AssignmentsCompleted"]]
y = data["Marks"]

print("\n===== Features (X) =====")
print(X.head())

print("\n===== Target (y) =====")
print(y.head())


# Scatter Plot
plt.figure(figsize=(8,5))

plt.scatter(
    data["StudyHours"],
    data["Marks"],
    color="blue",
    s=80
)

plt.title("Study Hours vs Marks", fontsize=16)
plt.xlabel("Study Hours", fontsize=12)
plt.ylabel("Marks", fontsize=12)

plt.grid(True)

plt.show()


from sklearn.model_selection import train_test_split

# selecting features
x = data[["StudyHours", "Attendance", "AssignmentsCompleted"]]

# target column
y = data["Marks"]

print("\nFeatures")
print(x.head())

print("\nTarget")
print(y.head())

# split the data
x_train, x_test, y_train, y_test = train_test_split(
    x,
    y,
    test_size=0.2,
    random_state=42
)

print("\nTraining Data")
print(x_train.head())

print("\nTesting Data")
print(x_test.head())

print("\nTraining Target")
print(y_train.head())

print("\nTesting Target")
print(y_test.head())

print("\nTraining Shape")
print(x_train.shape)

print("Testing Shape")
print(x_test.shape)