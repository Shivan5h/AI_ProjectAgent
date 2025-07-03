import streamlit as st

# Set page config
st.set_page_config(
    page_title="AI Coding Assistant",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Sidebar navigation
st.sidebar.title("AI Coding Assistant")
app_mode = st.sidebar.radio("Select Feature", 
                           ["Code Writer", "Code Reviewer", "Project Assistant"])

# Import the appropriate module based on selection
if app_mode == "Code Writer":
    from code_writer import show_code_writer
    show_code_writer()
elif app_mode == "Code Reviewer":
    from code_reviewer import show_code_reviewer
    show_code_reviewer()
elif app_mode == "Project Assistant":
    from project_assistant import show_project_assistant
    show_project_assistant()