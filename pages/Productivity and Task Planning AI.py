import streamlit as st
from groq import Groq

# Replace 'your_api_key_here' with your actual Groq API key
API_KEY = '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'
client = Groq(api_key=API_KEY)

# Function to generate AI responses for task planning
def generate_response(prompt):
    try:
        chat_completion = client.chat.completions.create(
            messages=[
                {
                    "role": "user",
                    "content": prompt,
                }
            ],
            model="llama3-8b-8192",
        )
        return chat_completion.choices[0].message.content
    except Exception as e:
        return f'Failed to generate response: {e}'

# Placeholder for storing tasks
if 'tasks' not in st.session_state:
    st.session_state.tasks = []

# Function to add a task
def add_task(task_name, task_details, due_date, priority, response):
    task = {
        'name': task_name,
        'details': task_details,
        'due_date': due_date,
        'priority': priority,
        'response': response.split('\n')
    }
    st.session_state.tasks.append(task)

# Function to remove a task
def remove_task(index):
    st.session_state.tasks.pop(index)

# Streamlit app interface
st.title("Productivity and Task Planning AI")

# Input fields for task creation
task_name = st.text_input("Task Name")
task_details = st.text_area("Task Details")
due_date = st.date_input("Due Date")
priority = st.slider("Priority (1 is highest, 10 is lowest)", 10, 1, 5)  # Priority slider

if st.button("Create Task"):
    prompt = f"Create a task named '{task_name}' with the following details: '{task_details}', a due date of {due_date}, and a priority of {priority}. Explain how to prioritize and plan it effectively, in three lines point form."
    response = generate_response(prompt)
    add_task(task_name, task_details, str(due_date), priority, response)

# Ensure all tasks have a 'priority' key
for task in st.session_state.tasks:
    if 'priority' not in task:
        task['priority'] = 3  # Default priority if not set

# Sort tasks by priority (highest priority first)
st.session_state.tasks = sorted(st.session_state.tasks, key=lambda x: x['priority'])

# Display tasks as sticky notes
st.subheader("Sticky Notes")
cols = st.columns(4)
for i, task in enumerate(st.session_state.tasks):
    with cols[i % 4]:
        st.markdown(f"### {task['name']}")
        st.markdown(f"**Details:** {task['details']}")
        st.markdown(f"**Due Date:** {task['due_date']}")
        st.markdown(f"**Priority:** {task['priority']}")
        st.markdown(f"**Planning:**")
        for j, point in enumerate(task['response']):
            # Ensure unique key for each checkbox
            checkbox_key = f"{task['name']}_{j}"
            st.checkbox(point.strip(), key=checkbox_key)
        if st.button(f"Remove {task['name']}", key=f"remove_{i}"):
            remove_task(i)
            st.experimental_rerun()