import streamlit as st
from groq import Groq

API_KEY = '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'
client = Groq(api_key=API_KEY)

# Function to generate AI responses for actions
def generate_actions(action):
    prompt = f"Provide a list of actions that can be taken to save money and increase sustainability for the following action: {action}. Only list the actions WITHOUT any explanations."
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
        return f'Failed to generate actions: {e}'

# Streamlit app interface
def main():
    st.title("Sustainability and Money Saving AI")

    # Input for user action
    user_action = st.text_input("Enter an action to get advice")

    # Button to get advice
    if st.button("Get Advice"):
        if user_action:
            actions = generate_actions(user_action)
            st.write("Here are some suggested actions:")
            actions_list = actions.split('\n')
            for action in actions_list:
                if action.strip():
                    st.checkbox(action.strip())
        else:
            st.write("Please enter an action to get advice.")

if __name__ == "__main__":
    main()
