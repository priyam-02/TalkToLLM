# 🤖 TalkToLLM Chat App

An interactive ChatGPT-style interface built with **Streamlit** and **FastAPI**, enabling real-time conversations with locally hosted LLMs using **Ollama** (e.g., LLaMA3, DeepSeek, Qwen2.5). Supports dynamic model selection, custom system prompts, streamed responses, and chat export in multiple formats.

---

## 🧩 Features

- 🧠 **System Prompt Setup** – Customize the assistant's role/personality
- 🔄 **Multiple LLMs** – Choose between `llama3.1`, `qwen2.5-coder`, and `deepseek-r1`
- 💬 **Custom LLM Support** – Pull and run **any local LLM** from Ollama, then update the model list in code:

  1. Pull any model using Ollama:

     ```bash
     ollama pull mistral
     ollama pull codellama
     ollama pull llama2
     ```

  2. Update this part of `app.py` to reflect the models you've pulled:

     ```python
     model = st.sidebar.selectbox(
         "Choose a model",
         ["llama3.1", "qwen2.5-coder", "deepseek-r1", "mistral", "codellama"]
     )
     ```

  3. That’s it — the app will automatically call the selected local model!

- 📤 **Live Streaming UI** – Chat responses streamed chunk-by-chunk like ChatGPT
- 🧠 **<think> Tag Support** – Visual differentiation of "thinking" and final responses for Deepseek-R1
- 💾 **Chat Export** – Save conversations as `.txt`, `.md`, or `.json`
- 🧹 **Clear Chat** – Reset conversation from the sidebar

---

## 📁 Project Structure

```
TalkToLLM/
├── frontend/
│   └── app.py              # Streamlit app
│   └── .streamlit/
│       └── config.toml     # Theme and layout config
├── backend/
│   └── main.py             # FastAPI server streaming Ollama responses
├── requirements.txt        # All required Python packages
└── README.md               # This file
```

---

## 🚀 Setup Instructions

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/llm_chat_app.git
cd llm_chat_app
```

### 2. Create & Activate Virtual Environment

```bash
python -m venv llm-chat-env
source llm-chat-env/bin/activate  # On Windows: llm-chat-env\Scripts\activate
```

### 3. Install Requirements

```bash
pip install -r requirements.txt
```

---

## ⚙️ Ollama Setup (for Local LLMs)

> Required for running the FastAPI backend with real models like `llama3`, `deepseek`, etc.

1. Download and install Ollama:  
   👉 https://ollama.com/download

2. Pull the required models:

```bash
ollama pull llama3
ollama pull deepseek
ollama pull qwen:2b
```

---

## 🖥️ Run the App

### ✅ Step 1: Start the Backend (FastAPI)

```bash
cd backend
uvicorn main:app --reload
```

This runs at: `http://localhost:8000`

---

### ✅ Step 2: Start the Frontend (Streamlit)

Open a new terminal and run:

```bash
cd frontend
streamlit run app.py
```

> App will launch in your browser at `http://localhost:8501`

---

## 📄 Exported Chat Sample

You can download conversations from the sidebar in:

- `.txt` – Simple transcript
- `.md` – Markdown formatted
- `.json` – Structured export

---

## 📬 Contact

Built with ❤️ by [Priyam Shah](https://github.com/priyam-02)  
Let’s connect on [LinkedIn](https://www.linkedin.com/in/priyamshah22/)
