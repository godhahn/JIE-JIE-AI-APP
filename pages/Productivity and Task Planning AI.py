import streamlit as st
import json
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

# Function to save tasks to file
def save_tasks(tasks):
    with open("tasks.json", "w") as f:
        json.dump(tasks, f)

# Function to load tasks from file
def load_tasks():
    try:
        with open("tasks.json", "r") as f:
            tasks = json.load(f)
            # Ensure 'checked_points' key exists for each task
            for task in tasks:
                if 'checked_points' not in task:
                    task['checked_points'] = [False] * len(task.get('response', []))
            return tasks
    except FileNotFoundError:
        return []

# Placeholder for storing tasks
if 'tasks' not in st.session_state:
    st.session_state.tasks = load_tasks()

# Function to add a task
def add_task(task_name, task_details, due_date, priority, response):
    task = {
        'name': task_name,
        'details': task_details,
        'due_date': due_date,
        'priority': priority,
        'response': response.split('\n'),
        'checked_points': [False] * len(response.split('\n'))  # Initialize all points as unchecked
    }
    st.session_state.tasks.append(task)
    save_tasks(st.session_state.tasks)

# Function to remove a task
def remove_task(index):
    st.session_state.tasks.pop(index)
    save_tasks(st.session_state.tasks)

# Function to move task to bottom (strike off)
def move_to_bottom(index):
    task = st.session_state.tasks.pop(index)
    task['name'] = f"~~{task['name']}~~"  # Strike off the task name
    task['priority'] = 5  # Set priority to the lowest value
    st.session_state.tasks.append(task)
    save_tasks(st.session_state.tasks)

# Function to update task details
def update_task_details(task_index, new_details):
    st.session_state.tasks[task_index]['details'] = new_details
    save_tasks(st.session_state.tasks)

# Streamlit app interface
st.title("Productivity and Task Planning AI")

st.markdown("---")
st.header("Generate Sticky Notes")

# Input fields for task creation
task_name = st.text_input("Task Name", max_chars=100, value='', help='Max 100 characters')
task_details = st.text_area("Task Details", value='', height=150, help='Use checkboxes for planning')

# Priority slider
priority = st.slider("Priority (1 is highest, 5 is lowest)", 1, 5, 3)

if st.button("Create Task"):
    prompt = f"With a task named '{task_name}', and the following details: '{task_details}', and a priority of {priority} (1 is highest, 5 is lowest). Give some additional information about the task AND Explain how to plan it effectively, in point form."
    response = generate_response(prompt)
    add_task(task_name, task_details, "", priority, response)

# Ensure all tasks have a 'priority' key
for task in st.session_state.tasks:
    if 'priority' not in task:
        task['priority'] = 5  # Default priority if not set

# Sort tasks by priority (highest priority first)
st.session_state.tasks = sorted(st.session_state.tasks, key=lambda x: x['priority'], reverse=True)

# Display tasks as collapsible sections
st.markdown("---")
st.header("Sticky Notes Wall")
for task in reversed(st.session_state.tasks):  # Display highest priority first
    with st.expander(task['name'], expanded=False):  # Collapsible expander for each task
        st.markdown(f"**Details:** {task['details']}", unsafe_allow_html=True)
        st.markdown(f"**Priority:** {task['priority']}")
        st.markdown(f"**Planning:**")
        
        # Display planning points as text
        for point in task['response']:
            st.text(point.strip())

        # Buttons for task management
        col1, col2 = st.columns([1, 1])
        with col1:
            if st.button(f"Remove {task['name']}"):
                remove_task(st.session_state.tasks.index(task))
        with col2:
            if st.button(f"Strike Off {task['name']}"):
                move_to_bottom(st.session_state.tasks.index(task))

        st.markdown("---")

        # Edit Sticky Note
        new_planning = st.text_area("Edit Sticky Note", value="\n".join(task['response']), height=100, key=f"edit_{task['name']}_planning")
        if st.button("Update Sticky Note", key=f"update_{task['name']}"):
            st.session_state.tasks[st.session_state.tasks.index(task)]['response'] = new_planning.split('\n')
            save_tasks(st.session_state.tasks)
