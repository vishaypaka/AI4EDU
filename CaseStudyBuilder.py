import os
import json
import warnings
import streamlit as st
from groq import Groq
import fitz  # PyMuPDF
from docx import Document

warnings.filterwarnings('ignore')

# Load API Key
working_dir = os.path.dirname(os.path.abspath(__file__))
config_data = json.load(open(f"{working_dir}/config.json"))
GROQ_API_KEY = config_data["GROQ_API_KEY"]
os.environ["GROQ_API_KEY"] = GROQ_API_KEY
client = Groq(api_key=GROQ_API_KEY)

# Streamlit page setup
st.set_page_config(page_title="Case Study Builder", page_icon="📚", layout="centered")
st.title("📚 Case Study Builder for Program Manager Course")

uploaded_files = st.file_uploader("Upload related documents (PDF, Word, or Text files)", accept_multiple_files=True)

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

for message in st.session_state.chat_history:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

user_prompt = st.chat_input("Type your request or leave blank and click Generate if files are uploaded...")

# Function to extract text
def extract_text_from_file(file):
    text = ""
    if file.type == "application/pdf":
        try:
            with fitz.open(stream=file.read(), filetype="pdf") as doc:
                for page in doc:
                    text += page.get_text()
        except Exception as e:
            st.warning(f"Couldn't read PDF file {file.name}: {e}")
    elif file.type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
        try:
            docx_file = Document(file)
            for para in docx_file.paragraphs:
                text += para.text + "\n"
        except Exception as e:
            st.warning(f"Couldn't read Word file {file.name}: {e}")
    elif file.type.startswith("text/"):
        try:
            text = file.read().decode("utf-8")
        except Exception as e:
            st.warning(f"Couldn't read text file {file.name}: {e}")
    else:
        st.warning(f"Unsupported file type: {file.name}")
    return text

if uploaded_files or user_prompt:
    all_text = ""

    if uploaded_files:
        for file in uploaded_files:
            all_text += extract_text_from_file(file)

    system_prompt = (
        "You are a case study generator for a Department of Defense Program Manager course.\n"
        "Using the provided content, generate a case study following this structure:\n\n"
        "1. **Opening Paragraph**: Identify decision-maker, organization, date, location, problem trigger.\n"
        "2. **Background**: Organization details, context.\n"
        "3. **Specific Issue/Decision Point**: Dilemma the project manager faces.\n"
        "4. **Alternatives**: List 2–3 possible courses of action.\n"
        "5. **Conclusion**: Summarize the challenge without giving the solution.\n"
        "6. **Discussion Questions**: Suggest 3–5 questions to promote critical thinking."
    )

    messages = [{"role": "system", "content": system_prompt}]
    if all_text:
        messages.append({"role": "user", "content": all_text})
    elif user_prompt:
        messages.append({"role": "user", "content": user_prompt})

    if st.button("Generate Case Study") or user_prompt:
        st.chat_message("user").markdown(user_prompt if user_prompt else "Generate Case Study from Uploaded Files")
        st.session_state.chat_history.append({"role": "user", "content": user_prompt if user_prompt else "Generate Case Study"})

        with st.spinner("Building your case study..."):
            try:
                response = client.chat.completions.create(
                    model='llama-3.3-70b-versatile',
                    messages=messages,
                    max_tokens=4096
                )
                assistant_response = response.choices[0].message.content
                st.chat_message("assistant").markdown(assistant_response)
                st.session_state.chat_history.append({"role": "assistant", "content": assistant_response})
            except Exception as e:
                st.error(f"Error generating case study: {e}")
else:
    st.info("Upload files or enter a prompt to generate the case study.")
