import sqlite3

# Connect to the database
conn = sqlite3.connect('dsa_quiz.db')
cursor = conn.cursor()

print("Setting up the database... This will reset all existing data.")

# Drop old tables to ensure a clean slate
for table in ['quiz_history', 'users', 'mcq_questions', 'coding_questions', 'topics']:
    cursor.execute(f"DROP TABLE IF EXISTS {table}")

# Create fresh, simplified tables
print("Creating new tables...")
cursor.execute('''CREATE TABLE users (id INTEGER PRIMARY KEY, username TEXT NOT NULL UNIQUE)''') # Simplified users table
cursor.execute('''CREATE TABLE topics (id INTEGER PRIMARY KEY, name TEXT NOT NULL UNIQUE)''')
cursor.execute('''CREATE TABLE mcq_questions (id INTEGER PRIMARY KEY, topic_id INTEGER, difficulty TEXT NOT NULL, question_text TEXT NOT NULL, option_a TEXT NOT NULL, option_b TEXT NOT NULL, option_c TEXT NOT NULL, option_d TEXT NOT NULL, correct_option TEXT NOT NULL, explanation TEXT, FOREIGN KEY (topic_id) REFERENCES topics (id))''')
cursor.execute('''CREATE TABLE coding_questions (id INTEGER PRIMARY KEY, topic_id INTEGER, difficulty TEXT NOT NULL, language TEXT NOT NULL, question_title TEXT NOT NULL, question_description TEXT NOT NULL, boilerplate_code TEXT, test_cases TEXT NOT NULL, solution_code TEXT NOT NULL, FOREIGN KEY (topic_id) REFERENCES topics (id))''')

# Populate data using safe, parameterized queries
print("Populating data...")
cursor.execute("INSERT INTO topics (name) VALUES ('Arrays'), ('Strings'), ('Sorting')")

# MCQ Data
mcq_data = [
    (1, 'Basic', 'Which data structure is best for storing a simple list of items to be accessed by index?', 'Array', 'Hash Map', 'Queue', 'Tree', 'A', 'Arrays provide O(1) time complexity for index-based access.'),
    (1, 'Basic', 'What is the index of the first element in a standard Python list?', '1', '0', '-1', 'None', 'B', 'Python lists, like most arrays, are zero-indexed.'),
    (1, 'Basic', 'How do you add an element `x` to the end of a Python list `my_list`?', 'my_list.add(x)', 'my_list.push(x)', 'my_list.append(x)', 'add(my_list, x)', 'C', 'The append() method is used to add items to the end of a list.'),
    (1, 'Basic', 'What is the time complexity to append an element to a Python list?', 'O(1)', 'O(n)', 'O(log n)', 'O(n^2)', 'A', 'Appending to a list is an amortized O(1) operation.')
]
cursor.executemany("INSERT INTO mcq_questions (topic_id, difficulty, question_text, option_a, option_b, option_c, option_d, correct_option, explanation) VALUES (?,?,?,?,?,?,?,?,?)", mcq_data)

# Coding Question Data
coding_question_data = (
    1, 'Basic', 'Python',
    'Remove Duplicates',
    'Write a function that takes a list and returns a new list with duplicates removed, preserving the original order.',
    'def remove_duplicates(arr):\n    # Your code here\n    pass',
    '[{"input": [1, 2, 2, 3], "output": [1, 2, 3]}, {"input": [["a", "b", "a"]], "output": ["a", "b"]}]',
    'def remove_duplicates(arr):\n    return list(dict.fromkeys(arr))'
)
cursor.execute("INSERT INTO coding_questions (topic_id, difficulty, language, question_title, question_description, boilerplate_code, test_cases, solution_code) VALUES (?,?,?,?,?,?,?,?)", coding_question_data)

conn.commit()
conn.close()

print("\nDatabase setup complete and successful!")