import sqlite3

DATABASE = "student_predictions.db"

import os
def get_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn


def create_table():
    conn = get_connection()

    conn.execute("""
    CREATE TABLE IF NOT EXISTS predictions (

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        timestamp TEXT,

        study_hours REAL,

        attendance REAL,

        assignments INTEGER,

        predicted_marks REAL,

        performance TEXT

    )
    """)

    conn.commit()
    conn.close()



def insert_prediction(timestamp, study_hours, attendance,
                      assignments, predicted_marks, performance):

    print("✅ insert_prediction() called")

    conn = get_connection()

    conn.execute("""
        INSERT INTO predictions(
            timestamp,
            study_hours,
            attendance,
            assignments,
            predicted_marks,
            performance
        )
        VALUES (?, ?, ?, ?, ?, ?)
    """, (
        timestamp,
        study_hours,
        attendance,
        assignments,
        predicted_marks,
        performance
    ))
    conn.commit()
    # cursor = conn.execute("SELECT COUNT(*) FROM predictions")
    # print("Rows in database:", cursor.fetchone()[0])

    conn.close()


def get_predictions():

    conn = get_connection()
    
    rows = conn.execute("""
        SELECT *
        FROM predictions
        ORDER BY id DESC
    """).fetchall()
    
    conn.close()
    
    return rows


if __name__ == "__main__":
    create_table()
    print("Database created successfully.")