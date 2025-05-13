# 📚 AI Assisted Case Writer

A powerful AI-driven case creation tool designed for **Program Manager leadership courses**. This application uses **LLaMA 3.3**, **Whisper**, and **Streamlit** to help faculty and instructional designers generate structured educational cases from uploaded documents, audio, and video content.

---

## 🚀 Features

- 📝 **Generate structured cases** in 6 parts (Opening, Background, Focal Area, Key Decision, Alternatives, Conclusion)
- 📂 **Multi-format file upload** (PDF, DOCX, TXT, MP3, MP4, WAV, M4A)
- 🎙️ **Audio/Video transcription** using [Whisper](https://github.com/openai/whisper)
- 📊 **Auto-generated stakeholder matrix, perspectives, and assignment questions**
- 🧠 **Interactive chat** to refine or discuss the generated case
- 📄 **Download formatted output** as PDF or Word (.docx)
- ✏️ **Live editing** of the generated content within the app

---

## 🧰 Requirements

Install the following before running the app:

- Python 3.9+
- [FFmpeg](https://ffmpeg.org/download.html) (for audio transcription)
- [Groq API Key](https://console.groq.com) to use LLaMA-3.3

---

## 🔧 Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/vishaypaka/AI4EDU.git
   cd AI4EDU
## Install dependencies:
pip install -r requirements.txt

## Set up your config:
{
  "GROQ_API_KEY": "your_groq_api_key_here"
}
## Make sure FFmpeg is installed and in PATH
run ffmpeg -version in your terminal to check its installed

## Run the app
streamlit run your_app_file.py



