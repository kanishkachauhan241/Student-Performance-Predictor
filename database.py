import sqlite3

DATABASE = "student_predictions.db"
from datetime import datetime, timedelta

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


def search_predictions(
        search="",
        sort="newest",
        performance_filter="",
        date_filter=""
):
        
    conn = get_connection()
    query = "SELECT * FROM predictions WHERE 1=1"
    params = []

    if search:
        query += """
        AND (
            timestamp LIKE ?
            OR study_hours LIKE ?
            OR attendance LIKE ?
            OR assignments LIKE ?
            OR predicted_marks LIKE ?
            OR performance LIKE ?
        )
        """

        value = f"%{search}%"

        params.extend([value, value, value, value, value, value])

    if performance_filter:
        query += " AND performance = ?"
        params.append(performance_filter)

    if date_filter:
        today = datetime.now()
        if date_filter == "today":
            date_string = today.strftime("%d-%m-%Y")
            query += " AND timestamp LIKE ?"
            params.append(f"{date_string}%")

        elif date_filter == "7days":
            cutoff = (today - timedelta(days=7)).strftime("%d-%m-%Y") 
            query += " AND timestamp >= ?"
            params.append(cutoff)

        elif date_filter == "30days":      
            cutoff = (today - timedelta(days=30)).strftime("%d-%m-%Y") 
            query += " AND timestamp >= ?"
            params.append(cutoff) 


    if sort == "newest":
        query += " ORDER BY id DESC"

    elif sort == "oldest":
        query += " ORDER BY id ASC"

    elif sort == "highest":
        query += " ORDER BY predicted_marks DESC"

    elif sort == "lowest":
        query += " ORDER BY predicted_marks ASC"

    rows = conn.execute(query, params).fetchall()

    conn.close()

    return rows


def get_predictions_paginated(
        page,
        per_page,
        search="",
        sort="newest",
        performance_filter="",
        date_filter=""
):
    conn = get_connection()
    query = "SELECT * FROM predictions WHERE 1=1"
    params = []

    if search:
        query += """
        AND (
            timestamp LIKE ?
            OR study_hours LIKE ?
            OR attendance LIKE ?
            OR assignments LIKE ?
            OR predicted_marks LIKE ?
            OR performance LIKE ?
        )
        """

        value = f"%{search}%"
        params.extend([value, value, value, value, value, value])

    if performance_filter:
        query += " AND performance = ?"
        params.append(performance_filter)
    if date_filter=="today":
        today = datetime.now().strftime("%d-%m-%Y")
        query += " AND timestamp LIKE ?"
        params.append(f"{today}%")     

    if sort == "newest":
        query += " ORDER BY id DESC"
    elif sort == "oldest":
        query += " ORDER BY id ASC"
    elif sort == "highest":
        query += " ORDER BY predicted_marks DESC"
    elif sort == "lowest":
        query += " ORDER BY predicted_marks ASC"
    else:
        query += " ORDER BY id DESC"    

    query += " LIMIT ? OFFSET ?"

    params.append(per_page)
    params.append((page - 1) * per_page)

    rows = conn.execute(query, params).fetchall()

    conn.close()

    return rows


def count_predictions(
    search="",
    performance_filter="",
    date_filter=""
):
    conn = get_connection()
    query = "SELECT COUNT(*) FROM predictions WHERE 1=1"
    params = []

    # Search filter
    if search:
        query += """
        AND (
            timestamp LIKE ?
            OR study_hours LIKE ?
            OR attendance LIKE ?
            OR assignments LIKE ?
            OR predicted_marks LIKE ?
            OR performance LIKE ?
        )
        """
        value = f"%{search}%"

        params.extend([
            value,
            value,
            value,
            value,
            value,
            value
        ])
    # Performance filter
    if performance_filter:
        query += " AND performance = ?"
        params.append(performance_filter)

    # Date filter
    if date_filter:
        today = datetime.now()
        if date_filter == "today":
            date_string = today.strftime("%d-%m-%Y")
            query += " AND timestamp LIKE ?"
            params.append(f"{date_string}%")
        elif date_filter == "7days":
            cutoff = today - timedelta(days=7)
            query += " AND timestamp >= ?"
            params.append(cutoff)
        elif date_filter == "30days":
            cutoff = today - timedelta(days=30)
            query += " AND timestamp >= ?"
            params.append(cutoff)
    total = conn.execute(
        query,
        params
    ).fetchone()[0]
    conn.close()
    return total
def get_statistics():
    conn = get_connection()
    stats = conn.execute("""
        SELECT
            COUNT(*) AS total,
            MAX(predicted_marks) AS highest,
            AVG(predicted_marks) AS average
        FROM predictions
    """).fetchone()

    conn.close()

    return dict(stats)


def get_performance_distribution():
    conn = get_connection()
    rows = conn.execute("""
        SELECT
            performance,
            COUNT(*) AS total
        FROM predictions
        GROUP BY performance
    """).fetchall()

    conn.close()

    return rows


if __name__ == "__main__":
    create_table()
    print("Database created successfully.")