# 🚀 AI Project & Coding Assistant

A powerful all-in-one AI-powered Streamlit application that unifies three essential tools for developers:

* 🧠 **Code Writer**: Converts natural language prompts into fully functional Python, Java, or C++ programs.
* 🔍 **Code Reviewer**: Reviews your code professionally, identifying bugs, inefficiencies, security issues, and suggesting improvements with interactive explanations.
* 🧱 **Project Assistant**: Understands and modifies entire codebases from GitHub repositories or local folders with a chat-based AI interface.

---

## 🧰 Features

### ✅ Code Writer

* Supports **Python**, **Java**, and **C++**
* Generates complete programs with:

  * All required imports
  * Main functions or entry points
  * Example usage & test cases
  * Logical comments and explanations
* Executes and displays output within the app

### ✅ Code Reviewer

* Supports multiple languages: `Python`, `JavaScript`, `Java`, `C++`, `Go`
* Detailed reviews covering:

  * Code quality
  * Bugs and edge cases
  * Performance tips
  * Security risks
  * Suggested improvements
* Hoverable in-code tooltips with simplified explanations
* Choice of review tone (professional, friendly, detailed, concise)

### ✅ Project Assistant

* Load projects from **GitHub** or **local folders**
* Understand complex codebases with contextual Q\&A
* Modify projects based on natural language requests
* Displays complete **project directory structure**
* Uses **ChromaDB** + **HuggingFace Embeddings** for code chunk indexing
* Integrated memory for chat history (session-based)

---

## 🛠️ Tech Stack

* **Frontend/UI**: Streamlit
* **LLMs**: Groq (`llama3-8b`, `mixtral-8x7b`, `llama2-70b`)
* **Code Gen**: LangChain + OpenAI Agents
* **Vector Store**: ChromaDB
* **Embeddings**: HuggingFace (`all-MiniLM-L6-v2`)
* **Execution Engine**: Python subprocesses for Java/C++/Python
* **Git Integration**: GitPython

---

## 📦 Installation

1. **Clone this repo**

```bash
git clone https://github.com/Shivan5h/AI_ProjectAgent
cd ai-project-coding-assistant
```

2. **Install dependencies**

```bash
pip install -r requirements.txt
```

3. **Set your API keys**

* Create a `.streamlit/secrets.toml` file:

```toml
OPENAI_API_KEY = "your-openai-key"
GROQ_API_KEY = "your-groq-key"
```

4. **Run the app**

```bash
streamlit run app.py
```

---

## 🎮 Usage Instructions

* Navigate using the sidebar
* Choose **Code Writer**, **Code Reviewer**, or **Project Assistant**
* Follow on-screen instructions in each tool

---

## 💡 Example Use Cases

* Generate a complete Python program to solve a math puzzle
* Review and debug a JavaScript snippet for potential issues
* Load a GitHub repo and ask questions like:

  * "Where is the database connection configured?"
  * "Add error handling to all I/O operations"

---

## 📁 Supported Languages

* Code Writer: `Python`, `Java`, `C++`
* Code Reviewer: `Python`, `JavaScript`, `Java`, `C++`, `Go`
* Project Assistant: `.py`, `.js`, `.ts`, `.java`, `.go`, `.rs`, `.md`

---


## 👥 Contributors

Feel free to open pull requests and suggest improvements!

---

## 🧠 Future Enhancements

* Code auto-refactoring from natural language
* Fine-tuned LLM integration
* GitHub PR generation and file patching
* Dockerized deployment

> Built with ❤️ for developers who want AI-powered productivity.
