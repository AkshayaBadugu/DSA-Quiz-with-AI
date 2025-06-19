import streamlit as st
from streamlit_ace import st_ace
import database as db
import code_evaluator as ce

st.set_page_config(page_title="DSA AI Tutor", page_icon="🧑‍🏫", layout="wide")

# --- STATE MANAGEMENT ---
if 'user' not in st.session_state:
    st.session_state.user = None
if 'quiz_started' not in st.session_state:
    st.session_state.quiz_started = False
if 'submitted' not in st.session_state:
    st.session_state.submitted = False

# --- LOGIN SCREEN ---
if st.session_state.user is None:
    st.title("Welcome to the AI DSA Tutor 🧑‍🏫")
    st.header("Login")
    username = st.text_input("Enter your username to start or register:")
    if st.button("Login / Register"):
        if username:
            st.session_state.user = db.get_or_create_user(username)
            st.rerun()
        else:
            st.warning("Please enter a username.")
    st.stop() # Stop the app if not logged in

# --- MAIN APP (after login) ---
st.sidebar.title(f"Welcome, {st.session_state.user['username']}! 👋")
if st.sidebar.button("Logout"):
    st.session_state.user = None
    st.rerun()

st.title("AI-Powered DSA Tutor")

# --- QUIZ SELECTION ---
if not st.session_state.quiz_started:
    st.header("🎯 Set Up Your Quiz")
    topics = db.get_topics()
    topic_names = [t['name'] for t in topics]
    col1, col2, col3 = st.columns(3)
    with col1: selected_topic_name = st.selectbox("1. Choose a Topic:", topic_names)
    with col2: selected_difficulty = st.selectbox("2. Choose a Difficulty:", ["Basic", "Intermediate", "Advanced"])
    with col3: selected_language = st.selectbox("3. Choose a Language:", ["Python"])
    
    if st.button("🚀 Start Quiz", type="primary"):
        topic_id = [t['id'] for t in topics if t['name'] == selected_topic_name][0]
        mcqs, coding_qs = db.get_questions(topic_id, selected_difficulty, selected_language)
        
        if len(mcqs) < 4 or len(coding_qs) < 1:
            st.error("Not enough questions in the database for this selection. Please try another combination or add more questions.")
        else:
            st.session_state.questions = mcqs + coding_qs
            st.session_state.user_answers = {}
            st.session_state.quiz_started = True
            st.session_state.submitted = False
            st.rerun()

# --- QUIZ INTERFACE ---
elif not st.session_state.submitted:
    st.header("📝 Your Quiz")
    questions = st.session_state.questions
    with st.form(key='quiz_form'):
        for i, q in enumerate(questions):
            st.markdown("---")
            if 'question_text' in q.keys():
                st.subheader(f"Question {i+1}: Multiple Choice")
                st.write(q['question_text'])
                options = {'A': q['option_a'], 'B': q['option_b'], 'C': q['option_c'], 'D': q['option_d']}
                st.session_state.user_answers[q['id']] = st.radio("Your answer:", options.keys(), format_func=lambda x: f"{x}: {options[x]}", key=f"mcq_{q['id']}", horizontal=True)
            else:
                st.subheader(f"Question {i+1}: Coding Challenge")
                st.markdown(f"**{q['question_title']}**")
                st.markdown(q['question_description'])
                st.session_state.user_answers[q['id']] = st_ace(value=q['boilerplate_code'], language='python', theme='tomorrow_night_eighties', key=f"code_{q['id']}", height=250)
        
        if st.form_submit_button("✅ Submit Quiz"):
            st.session_state.submitted = True
            st.rerun()

# --- RESULTS SCREEN ---
else:
    st.header("📊 Results")
    questions = st.session_state.questions
    for q in questions:
        st.markdown("---")
        if 'question_text' in q.keys(): # MCQ Result
            st.subheader(f"MCQ: {q['question_text']}")
            user_ans = st.session_state.user_answers.get(q['id'])
            correct_ans = q['correct_option']
            if user_ans == correct_ans:
                st.success(f"✅ Correct! Your answer: {user_ans}")
            else:
                st.error(f"❌ Incorrect. Your answer: {user_ans}, Correct answer: {correct_ans}")
            with st.expander("See explanation"):
                st.info(q['explanation'])
        
        else: # Coding Result
            st.subheader(f"Coding: {q['question_title']}")
            user_code = st.session_state.user_answers.get(q['id'])
            
            with st.spinner("Analyzing your code..."):
                eval_result = ce.run_code_against_test_cases(user_code, q['test_cases'])
            
            if eval_result['status'] == 'All Tests Passed':
                st.success("🎉 Congratulations! All test cases passed.")
            else:
                st.error(f"🚨 Your code has an issue: **{eval_result['status']}**")
                st.json(eval_result['details']) # Show the details of the failure

    if st.button("Try Another Quiz"):
        st.session_state.quiz_started = False
        st.session_state.submitted = False
        st.rerun()