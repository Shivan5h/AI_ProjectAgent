import os
import streamlit as st
from groq import Groq
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings
from git import Repo
import tempfile
from pathlib import Path

def show_project_assistant():
    # Initialize Groq client
    client = Groq(api_key=os.getenv("GROQ_API_KEY"))

    # Configure embeddings
    embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

    # Session state setup
    if "messages" not in st.session_state:
        st.session_state.messages = []
    if "vectorstore" not in st.session_state:
        st.session_state.vectorstore = None
    if "project_path" not in st.session_state:
        st.session_state.project_path = None

    def clone_repo(repo_url):
        temp_dir = tempfile.mkdtemp()
        Repo.clone_from(repo_url, temp_dir)
        return temp_dir

    def load_project_files(project_path):
        code_files = []
        for root, _, files in os.walk(project_path):
            for file in files:
                if file.endswith((".py", ".js", ".ts", ".java", ".go", ".rs", ".md")):
                    file_path = os.path.join(root, file)
                    try:
                        with open(file_path, "r", encoding="utf-8") as f:
                            code_files.append({
                                "path": file_path,
                                "content": f.read()
                            })
                    except UnicodeDecodeError:
                        continue
        return code_files

    def create_vectorstore(files):
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200
        )
        
        texts = []
        metadatas = []
        
        for file in files:
            chunks = text_splitter.split_text(file["content"])
            for chunk in chunks:
                texts.append(chunk)
                metadatas.append({"source": file["path"]})
        
        return Chroma.from_texts(
            texts=texts,
            embedding=embeddings,
            metadatas=metadatas
        )

    def groq_chat_completion(prompt, context=""):
        full_prompt = f"""
        Project Context:
        {context}

        User Question:
        {prompt}

        Answer concisely and technically, always reference specific files when possible.
        """
        
        response = client.chat.completions.create(
            messages=[
                {
                    "role": "system",
                    "content": "You are an expert code explainer. Provide detailed technical answers based on the project context."
                },
                {
                    "role": "user",
                    "content": full_prompt
                }
            ],
            model="llama3-8b-8192",
            temperature=0.3,
            stream=True
        )
        return response

    def get_relevant_context(query):
        if st.session_state.vectorstore:
            docs = st.session_state.vectorstore.similarity_search(query, k=3)
            return "\n".join([f"File: {doc.metadata['source']}\nContent:\n{doc.page_content}" for doc in docs])
        return "No project loaded"

    # Streamlit UI
    st.title("Project Assistant")
    st.write("Understand and modify any code project with AI assistance")

    # Project input options
    input_method = st.radio("Project Source:", ("GitHub Repo", "Local Folder"))

    if input_method == "GitHub Repo":
        repo_url = st.text_input("GitHub Repository URL:")
        if repo_url and st.button("Load Repository"):
            with st.spinner("Cloning and analyzing repository..."):
                project_path = clone_repo(repo_url)
                st.session_state.project_path = project_path
                files = load_project_files(project_path)
                st.session_state.vectorstore = create_vectorstore(files)
                st.success(f"Loaded {len(files)} files from repository")

    else:
        local_path = st.text_input("Local Project Path:")
        if local_path and st.button("Load Local Project"):
            if os.path.exists(local_path):
                st.session_state.project_path = local_path
                files = load_project_files(local_path)
                st.session_state.vectorstore = create_vectorstore(files)
                st.success(f"Loaded {len(files)} files from local project")
            else:
                st.error("Path does not exist")

    # Chat interface
    if st.session_state.project_path:
        st.divider()
        st.subheader("Project Chat")
        
        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])
        
        if prompt := st.chat_input("Ask about the project..."):
            st.session_state.messages.append({"role": "user", "content": prompt})
            with st.chat_message("user"):
                st.markdown(prompt)
            
            with st.chat_message("assistant"):
                context = get_relevant_context(prompt)
                response = groq_chat_completion(prompt, context)
                
                full_response = st.empty()
                message_placeholder = st.empty()
                complete_response = ""
                
                for chunk in response:
                    if chunk.choices[0].delta.content:
                        complete_response += chunk.choices[0].delta.content
                        message_placeholder.markdown(complete_response + "▌")
                
                message_placeholder.markdown(complete_response)
                st.session_state.messages.append({"role": "assistant", "content": complete_response})
    else:
        st.info("Please load a project to start chatting")

    # Project modification section
    if st.session_state.project_path:
        st.divider()
        st.subheader("Project Modifications")
        
        modification_request = st.text_area("Request code changes (e.g., 'Add error handling to main.py')")
        
        if st.button("Generate Modification"):
            with st.spinner("Analyzing project for changes..."):
                context = get_relevant_context(modification_request)
                prompt = f"""
                Project Context:
                {context}

                Modification Request:
                {modification_request}

                Provide:
                1. Specific files that need changes
                2. Exact code changes needed
                3. Any dependencies to add
                """
                
                response = groq_chat_completion(prompt)
                
                modification_placeholder = st.empty()
                complete_modification = ""
                
                for chunk in response:
                    if chunk.choices[0].delta.content:
                        complete_modification += chunk.choices[0].delta.content
                        modification_placeholder.markdown(complete_modification + "▌")
                
                modification_placeholder.markdown(complete_modification)
                st.session_state.messages.append({
                    "role": "assistant",
                    "content": f"Modification suggestion:\n{complete_modification}"
                })

    # Display project structure
    if st.session_state.project_path:
        st.divider()
        if st.button("Show Project Structure"):
            project_structure = []
            for root, dirs, files in os.walk(st.session_state.project_path):
                level = root.replace(st.session_state.project_path, "").count(os.sep)
                indent = " " * 4 * (level)
                project_structure.append(f"{indent}{os.path.basename(root)}/")
                subindent = " " * 4 * (level + 1)
                for f in files:
                    project_structure.append(f"{subindent}{f}")
            
            with st.expander("Project Structure"):
                st.code("\n".join(project_structure))