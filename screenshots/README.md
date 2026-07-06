# Student Performance Predictor

This is my beginner Machine Learning project built using Python and Scikit-learn.

The project predicts a student's marks based on:
- Study Hours
- Attendance
- Assignments Completed

I created this project to practice the basic machine learning workflow, including data exploration, visualization, model training, prediction, and evaluation.

---

## Features

- Load and explore the dataset using Pandas
- Visualize data using Matplotlib
- Clean and prepare the dataset
- Train a Linear Regression model
- Predict marks for new students
- Save the trained model using Joblib
- Save prediction history to a CSV file
- Evaluate the model using MAE, MSE and R² Score

---

## Technologies Used

- Python
- Pandas
- Matplotlib
- Scikit-learn
- Joblib

---

## Project Structure

```
Student-Performance-Predictor/
│
├── data/
│   └── student_data.csv
├── src/
│   └── train_model.py
├── screenshots/
├── README.md
├── requirements.txt
└── .gitignore
```

---

## How to Run

Clone the repository

```bash
git clone <repository-link>
```

Install the required libraries

```bash
pip install -r requirements.txt
```

Run the project

```bash
python src/train_model.py
```

---

## Sample Output

```
Study Hours: 7
Attendance: 90
Assignments Completed: 8

Predicted Marks: 79.33
Performance: Very Good
```

---

## Future Improvements

- Build a Flask web application
- Use a larger dataset
- Try different machine learning algorithms
- Improve the user interface

---

## Learning Outcomes

Through this project I learned:
- Data exploration using Pandas
- Data visualization using Matplotlib
- Train-test splitting
- Linear Regression
- Model evaluation
- Saving and loading models with Joblib
- Basic Git and GitHub workflow

---

## Author

**Kanishka Chauhan**

Computer Science student learning Machine Learning by building projects.
