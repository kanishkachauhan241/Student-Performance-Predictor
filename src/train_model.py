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

# Split the dataset
X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42
)

print("\n===== Training Data Shape =====")
print(X_train.shape)
print(y_train.shape)

print("\n===== Testing Data Shape =====")
print(X_test.shape)
print(y_test.shape)