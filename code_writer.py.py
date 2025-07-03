import streamlit as st
from langchain.agents import initialize_agent, Tool
from langchain_openai import OpenAI
from langchain_experimental.tools import PythonREPLTool
import subprocess
import os

def run_python_code(code: str) -> str:
    try:
        local_vars = {}
        exec(code, {}, local_vars)
        return str(local_vars)
    except Exception as e:
        return f"Error executing Python code: {e}"

def run_java_code(code: str) -> str:
    try:
        with open("Main.java", "w") as f:
            f.write(code)
        subprocess.run(["javac", "Main.java"], check=True)
        result = subprocess.run(["java", "Main"], capture_output=True, text=True)
        return result.stdout + result.stderr
    except Exception as e:
        return f"Error executing Java code: {e}"

def run_cpp_code(code: str) -> str:
    try:
        with open("main.cpp", "w") as f:
            f.write(code)
        subprocess.run(["g++", "main.cpp", "-o", "main_exe"], check=True)
        result = subprocess.run(["./main_exe"], capture_output=True, text=True)
        return result.stdout + result.stderr
    except Exception as e:
        return f"Error executing C++ code: {e}"

def execute_code(language: str, code: str) -> str:
    if language == "Python":
        return run_python_code(code)
    elif language == "Java":
        return run_java_code(code)
    elif language == "C++":
        return run_cpp_code(code)
    else:
        return "Unsupported language."

def show_code_writer():
    # Load environment variables
    openai_api_key = st.secrets["OPENAI_API_KEY"]
    os.environ["OPENAI_API_KEY"] = openai_api_key

    # Supported languages
    SUPPORTED_LANGUAGES = ["Python", "Java", "C++"]

    # LangChain Agent Setup
    llm = OpenAI(temperature=0)
    tools = [
        Tool(
            name="PythonREPL",
            func=PythonREPLTool().run,
            description="Run Python code."
        )
    ]
    agent = initialize_agent(tools, llm, agent="zero-shot-react-description", verbose=True)

    # Streamlit UI
    st.title("Code Writer")
    st.write("Generate code using AI for your programming needs")

    language = st.selectbox("Select Programming Language", SUPPORTED_LANGUAGES)
    prompt = st.text_area("Enter your prompt for code generation")

    if st.button("Generate Code"):
        with st.spinner("Generating code..."):
            system_message = """You are a code generation assistant. Your task is to generate complete, runnable programs.
            Always include:
            1. All necessary imports
            2. A main function or entry point
            3. Example usage with test cases
            4. Comments explaining the logic
            Never return just the answer - always return the complete program."""
            
            full_prompt = f"""Write a complete {language} program that solves the following problem:
            {prompt}
            
            The program should:
            1. Include all necessary imports
            2. Have a main function or entry point
            3. Include example usage with test cases
            4. Have comments explaining the logic
            5. Be properly formatted
            
            Return the complete program code, not just the answer."""
            
            final_prompt = f"{system_message}\n\n{full_prompt}"
            
            code = agent.run(final_prompt)
            code = code.strip()
            if code.startswith("```"):
                code = code.split("```")[1]
            if code.endswith("```"):
                code = code.rsplit("```", 1)[0]
            code = code.strip()
            
            st.code(code, language=language.lower())
            st.session_state["generated_code"] = code
            st.session_state["selected_language"] = language

    if "generated_code" in st.session_state:
        st.divider()
        st.subheader("Test Generated Code")
        if st.button("Execute Code"):
            result = execute_code(
                st.session_state["selected_language"],
                st.session_state["generated_code"]
            )
            st.text_area("Execution Result", result, height=200)