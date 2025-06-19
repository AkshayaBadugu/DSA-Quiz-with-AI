# DSA-Quiz-with-AI
# 🧑‍🏫 AI-Powered DSA Quiz

An interactive web application built with Streamlit that allows users to practice Data Structures and Algorithms questions. The app features a simple login, personalized quiz generation based on topic and difficulty, and real-time code evaluation.

 

---

## ✨ Features

- **Simple User Authentication:** A basic username system to log in or register.
- **Personalized Quiz Setup:** Users can select:
  - **Topic** (e.g., Arrays, Strings)
  - **Difficulty** (e.g., Basic, Intermediate)
  - **Language** (Python)
- **Mixed-Type Quizzes:** Each quiz consists of multiple-choice questions (MCQs) and a hands-on coding challenge.
- **Real-time Code Evaluation:** User-submitted Python code is run against hidden test cases to check for correctness.
- **Instant Feedback:** The app provides immediate results, explanations for MCQs, and pass/fail status for coding problems.

---

## 🛠️ Tech Stack

- **Frontend:** [Streamlit](https://streamlit.io/) - For building the interactive web UI.
- **Code Editor:** [Streamlit Ace](https://github.com/okld/streamlit-ace) - For the in-browser code editor.
- **Backend Logic:** Python
- **Database:** [SQLite](https://www.sqlite.org/index.html) - For storing users, topics, and questions.
- **Code Execution:** Python's built-in `subprocess` module.

---

## 🚀 How to Run This Project Locally

Follow these steps to get the project running on your local machine.

### **Prerequisites**

- Python 3.8 or higher installed on your system.
- `pip` (Python package installer).

### **Installation & Setup**

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/AkshayaBadugu/your-repository-name.git
    ```

2.  **Navigate into the project directory:**
    ```bash
    cd your-repository-name
    ```

3.  **Install the required dependencies:**
    *(It is recommended to create a virtual environment first)*
    ```bash
    pip install streamlit streamlit-ace
    ```

4.  **Set up the database for the first time:**
    This script will create the `dsa_quiz.db` file and populate it with sample questions.
    ```bash
    python setup_database.py
    ```

5.  **Run the Streamlit application:**
    ```bash
    streamlit run app.py
    ```

The application should now be open and running in your web browser!

---

## 📁 Project Structure
