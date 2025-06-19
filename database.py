import sqlite3

def get_db_connection():
    conn = sqlite3.connect('dsa_quiz.db')
    conn.row_factory = sqlite3.Row
    return conn

def get_or_create_user(username):
    """Finds a user by username or creates a new one. Returns the user object."""
    conn = get_db_connection()
    user = conn.execute('SELECT * FROM users WHERE username = ?', (username,)).fetchone()
    if user is None:
        cursor = conn.cursor()
        cursor.execute('INSERT INTO users (username) VALUES (?)', (username,))
        conn.commit()
        user_id = cursor.lastrowid
        user = conn.execute('SELECT * FROM users WHERE id = ?', (user_id,)).fetchone()
    conn.close()
    return user

def get_questions(topic_id, difficulty, language, num_mcq=4, num_coding=1):
    conn = get_db_connection()
    mcqs = conn.execute('SELECT * FROM mcq_questions WHERE topic_id = ? AND difficulty = ? ORDER BY RANDOM() LIMIT ?', (topic_id, difficulty, num_mcq)).fetchall()
    coding_questions = conn.execute('SELECT * FROM coding_questions WHERE topic_id = ? AND difficulty = ? AND language = ? ORDER BY RANDOM() LIMIT ?', (topic_id, difficulty, language, num_coding)).fetchall()
    conn.close()
    return mcqs, coding_questions

def get_topics():
    conn = get_db_connection()
    topics = conn.execute('SELECT * FROM topics').fetchall()
    conn.close()
    return topics