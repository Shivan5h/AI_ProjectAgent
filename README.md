# 🧠 Agentic Project Explainer

A powerful agentic AI tool that helps you understand, explore, and modify code projects. Whether the project is located on GitHub or on your local machine, this agent can:

* Load and analyze the entire codebase
* Answer technical questions with code-level context
* Suggest code modifications
* Visualize project structure
* Remember Q\&A interactions during the session

---

## 🚀 Features

* 🔍 **Understand Projects**: Get contextual, file-referenced answers for any technical query.
* 📂 **Supports GitHub & Local Projects**: Input a GitHub repo URL or select a local project folder.
* 💬 **Interactive Q\&A**: Ask anything about the project with live streaming responses using Groq (LLaMA 3).
* 🧠 **Session Memory**: Remembers your questions and answers for the current session (cleared when server stops).
* 🛠️ **Code Modification Assistant**: Get suggestions for code changes with precise file references.
* 🗂️ **Project Structure Viewer**: Explore the directory tree of your project.

---

## 🏗️ Tech Stack

* **Frontend/UI**: Streamlit
* **LLM API**: Groq (LLaMA3-8b-8192)
* **Embeddings**: HuggingFace `all-MiniLM-L6-v2`
* **Vector Store**: ChromaDB
* **Text Splitting**: RecursiveCharacterTextSplitter
* **Git Integration**: GitPython

---

## 🔧 How It Works

1. **Project Loading**

   * GitHub: Clone repo using GitPython into a temporary directory.
   * Local: Load directory from user path input.

2. **File Processing**

   * Parses `.py`, `.js`, `.ts`, `.java`, `.go`, `.rs`, `.md` files.
   * Chunks content and stores it in a Chroma vectorstore.

3. **Project Q\&A**

   * Retrieves relevant context using vector similarity search.
   * Sends full prompt with context to Groq's LLM.
   * Displays streamed response and logs in session memory.

4. **Modification Requests**

   * Generates modification steps including which files to update, exact code changes, and dependencies.

5. **Session Memory**

   * Q\&A log persists until the Streamlit session is closed.

---

## 🧪 Usage Instructions

1. Install requirements:

```bash
pip install -r requirements.txt
```

2. Set your Groq API key:

```bash
export GROQ_API_KEY=your_key_here
```

3. Run the app:

```bash
streamlit run app.py
```

---

## 📁 File Types Supported

* `.py`, `.js`, `.ts`, `.java`, `.go`, `.rs`, `.md`

---

## 💡 Example Queries

* "What does `main.py` do?"
* "How is authentication handled in the project?"
* "Add logging to all database-related functions."
* "Which files define the API endpoints?"

---

## 🛑 Limitations

* Session memory is volatile (cleared when app stops)
* Does not modify files automatically—suggests code only

---


## 🤝 Contributions

Open to suggestions, ideas, and PRs!
