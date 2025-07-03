import streamlit as st
import groq
from groq import Groq
from pygments import highlight
from pygments.lexers import PythonLexer, get_lexer_by_name
from pygments.formatters import HtmlFormatter
import html
import re

def show_code_reviewer():
    # Initialize Groq client
    client = Groq(api_key=st.secrets["GROQ_API_KEY"])

    # Sidebar for configuration
    with st.sidebar:
        st.header("Configuration")
        language = st.selectbox("Programming Language", ["python", "javascript", "java", "c++", "go"])
        review_style = st.selectbox("Review Style", ["professional", "friendly", "detailed", "concise"])
        model_name = st.selectbox("AI Model", ["mixtral-8x7b-32768", "llama2-70b-4096"])

    # Initialize session state for hover explanations
    if "hover_explanations" not in st.session_state:
        st.session_state.hover_explanations = {}

    def get_code_review(code, language, style):
        prompt = f"""
        You are an expert {language} code reviewer. Analyze the following code and provide a {style} review:
        
        Code:
        {code}
        
        Review should cover:
        1. Code quality and style
        2. Potential bugs or issues
        3. Performance considerations
        4. Security concerns
        5. Suggested improvements
        
        Format your response with clear headings for each section.
        """
        
        try:
            chat_completion = client.chat.completions.create(
                messages=[{"role": "user", "content": prompt}],
                model=model_name,
                temperature=0.3,
            )
            return chat_completion.choices[0].message.content
        except Exception as e:
            return f"Error getting review: {str(e)}"

    def get_code_explanations(code, language):
        chunks = split_code_into_chunks(code, language)
        explanations = {}
        for chunk_id, chunk in chunks.items():
            prompt = f"""
            Explain this {language} code snippet in simple terms:
            
            {chunk}
            
            Your explanation should:
            1. Describe what this code does
            2. Explain key components
            3. Be concise (1-2 paragraphs max)
            4. Use simple language
            """
            
            try:
                chat_completion = client.chat.completions.create(
                    messages=[{"role": "user", "content": prompt}],
                    model=model_name,
                    temperature=0.1,
                )
                explanations[chunk_id] = chat_completion.choices[0].message.content
            except Exception as e:
                explanations[chunk_id] = f"Error getting explanation: {str(e)}"
        return explanations

    def split_code_into_chunks(code, language):
        chunks = {}
        if language == "python":
            parts = re.split(r'(def \w+\(.*?\):|class \w+:)', code)
            for i in range(1, len(parts), 2):
                chunk_name = parts[i].strip()
                chunk_content = parts[i] + parts[i+1]
                chunks[chunk_name] = chunk_content
        else:
            lines = code.split('\n')
            for i, line in enumerate(lines):
                if line.strip():
                    chunks[f"line_{i+1}"] = line
        return chunks

    def generate_code_html(code, explanations, language):
        try:
            lexer = get_lexer_by_name(language)
        except:
            lexer = PythonLexer()
        
        formatter = HtmlFormatter(style="friendly", linenos=True)
        highlighted_code = highlight(code, lexer, formatter)
        css = formatter.get_style_defs('.highlight')
        
        for chunk_id, explanation in explanations.items():
            safe_explanation = html.escape(explanation)
            if chunk_id.startswith("line_"):
                line_num = int(chunk_id.split("_")[1])
                highlighted_code = highlighted_code.replace(
                    f'<span class="lineno">{line_num} </span>',
                    f'<span class="lineno">{line_num} </span><span class="hoverable" title="{safe_explanation}">'
                )
            else:
                highlighted_code = highlighted_code.replace(
                    chunk_id,
                    f'<span class="hoverable" title="{safe_explanation}">{chunk_id}</span>'
                )
        
        css += """
        .hoverable {
            position: relative;
            border-bottom: 1px dotted #666;
            cursor: help;
        }
        .hoverable:hover::after {
            content: attr(title);
            position: absolute;
            left: 0;
            top: 100%;
            z-index: 1000;
            background: #ffffee;
            border: 1px solid #ccc;
            padding: 8px;
            width: 300px;
            box-shadow: 2px 2px 5px rgba(0,0,0,0.3);
            color: #333;
            font-size: 14px;
            white-space: pre-wrap;
        }
        """
        
        return f"<style>{css}</style>{highlighted_code}"

    # Main app
    st.title("Code Reviewer")
    st.write("Analyze and understand your code with AI-powered review")

    col1, col2 = st.columns([1, 1])

    with col1:
        st.subheader("Enter Your Code")
        code_input = st.text_area("Paste your code here", height=400, key="code_input")
        
        if st.button("Analyze Code"):
            if code_input.strip():
                with st.spinner("Getting code review and explanations..."):
                    review = get_code_review(code_input, language, review_style)
                    st.session_state.hover_explanations = get_code_explanations(code_input, language)
                    st.session_state.review = review
                    st.session_state.code = code_input
            else:
                st.warning("Please enter some code to analyze")

    with col2:
        st.subheader("Code Review")
        if "review" in st.session_state:
            st.markdown(st.session_state.review)
        
        st.subheader("Interactive Code")
        if "code" in st.session_state and "hover_explanations" in st.session_state:
            code_html = generate_code_html(
                st.session_state.code,
                st.session_state.hover_explanations,
                language
            )
            st.components.v1.html(code_html, height=400, scrolling=True)