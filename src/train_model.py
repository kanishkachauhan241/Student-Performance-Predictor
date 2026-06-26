import pandas as pd

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