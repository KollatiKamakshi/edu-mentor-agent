import streamlit as st
from project.main_agent import run_agent

def run_app():
    """A simple Streamlit interface mock for Hugging Face deployment."""
    st.title("📚 EduMentor: Personalized Learning Path Generator")
    st.markdown("Agents for Good Capstone Project - **Planner -> Worker -> Evaluator**")

    user_goal = st.text_input(
        "Enter your learning goal:",
        "Learn Python basics for web development"
    )

    if st.button("Generate Learning Path"):
        if user_goal:
            with st.spinner("Agents are curating your path..."):
                try:
                    # Execute the multi-agent system
                    path_result = run_agent(user_goal)
                    st.text_area("Generated Path", path_result, height=500)
                except Exception as e:
                    st.error(f"An error occurred during agent execution: {e}")
        else:
            st.warning("Please enter a learning goal.")

if __name__ == '__main__':
    # This block is for running the Streamlit app locally or on Hugging Face.
    # In Colab, we simulate the run below.
    # st.run_app()
    print("Run `!streamlit run project/app.py` in a terminal to start the app.")
