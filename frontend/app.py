import time
import streamlit as st
import requests
from datetime import datetime


st.set_page_config(page_title="Chat with Local LLM", page_icon="🤖")
st.title("🤖 Local LLM Chat App")

st.sidebar.markdown("🤖 **Model**")

# 🔁 Model selection
model = st.sidebar.selectbox(
    "Choose a model", ["llama3.1", "qwen2.5-coder", "deepseek-r1"]
)
st.sidebar.markdown("---")
st.sidebar.markdown("🧠 **System Prompt (Optional)**")
default_system_prompt = "You are a helpful and concise assistant."
system_prompt = st.sidebar.text_area(
    "Customize the assistant's behavior:",
    value=default_system_prompt,
    height=100,
)
if system_prompt != "You are a helpful and concise assistant.":
    st.markdown(f"🔧 **System Prompt Active:** {system_prompt}")

# 🧠 Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Handle chat input
prompt = st.chat_input("Ask anything...")

# ⬇️ First, render all completed messages
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# 🧍 If user sends a new prompt
if prompt:
    # Add user message
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        thinking_mode = False
        has_thinking = False
        response_placeholder = st.empty()
        final_answer_placeholder = st.empty()

        # ✅ Typing indicator shown where final answer will go
        final_answer_placeholder.markdown("💬 *Assistant is typing.*")
        time.sleep(0.5)
        final_answer_placeholder.markdown("💬 *Assistant is typing..*")
        time.sleep(0.5)
        final_answer_placeholder.markdown("💬 *Assistant is typing...*")

        thinking_buffer = ""
        answer_buffer = ""

        try:
            r = requests.post(
                "http://localhost:8000/query_llm_stream",
                json={
                    "model": model,
                    "messages": [{"role": "system", "content": system_prompt}]
                    + st.session_state.messages,
                },
                stream=True,
            )
            for chunk in r.iter_content(chunk_size=64):
                if chunk:
                    part = chunk.decode("utf-8")

                    # Start streaming <think> content
                    if "<think>" in part:
                        thinking_mode = True
                        has_thinking = True
                        part = part.split("<think>", 1)[1]

                    if "</think>" in part:
                        thinking_mode = False
                        split_part = part.split("</think>", 1)
                        thinking_buffer += split_part[0]
                        part = split_part[1]
                        response_placeholder.markdown(
                            f"""
    <div style='background-color: #f0f0f0; padding: 12px; border-radius: 8px; margin-bottom: 10px;'>
        <strong>🤔 Thinking:</strong><br>{thinking_buffer.replace('\n', '<br>')}
    </div>
    """,
                            unsafe_allow_html=True,
                        )
                    else:
                        if thinking_mode:
                            thinking_buffer += part
                            response_placeholder.markdown(
                                f"""
                                <div style='background-color: #f0f0f0; padding: 12px; border-radius: 8px; margin-bottom: 10px;'>
                                    <strong>🤔 Thinking:</strong><br>{thinking_buffer.replace('\n', '<br>')}
                                </div>
                                """,
                                unsafe_allow_html=True,
                            )
                        else:
                            answer_buffer += part
                            final_answer_placeholder.markdown(answer_buffer)

        except Exception as e:
            final_answer_placeholder.markdown(f"❌ Error: {str(e)}")

        # 🧠 Store full response in memory (combine both buffers)
        if has_thinking:
            combined = f"🤔 *Thinking hidden*\n\n{answer_buffer.strip()}"
        else:
            combined = answer_buffer.strip()

        st.session_state.messages.append({"role": "assistant", "content": combined})

# 🧠 Include system prompt if it's set
if system_prompt.strip():
    system_prompt_text = f"System Prompt:\n{system_prompt.strip()}\n\n"
else:
    system_prompt_text = ""

#     # 📥 Prepare downloadable chat content
# if st.session_state.get("messages"):
#     chat_text = "\n\n".join(
#         [
#             f"{m['role'].capitalize()}:\n{m['content']}"
#             for m in st.session_state.messages
#         ]
#     )
# else:
#     chat_text = "No messages yet."

# # 🔗 Final download content
# full_export = system_prompt_text + chat_text

st.sidebar.markdown("---")

st.sidebar.markdown("📄 **Export**")


file_format = st.sidebar.selectbox("Select format", ["TXT", "Markdown", "JSON"])
# 🧾 Build export content based on format
if st.session_state.get("messages"):
    if file_format == "TXT":
        content = "\n\n".join(
            [
                f"{m['role'].capitalize()}:\n{m['content']}"
                for m in st.session_state.messages
            ]
        )
        full_export = f"Model Used: {model}\n\n{system_prompt_text}\n{content}"
        mime_type = "text/plain"
        extension = "txt"

    elif file_format == "Markdown":
        content = "\n\n".join(
            [
                f"### {m['role'].capitalize()}\n{m['content']}"
                for m in st.session_state.messages
            ]
        )
        full_export = f"# Model Used: {model}\n\n## System Prompt\n{system_prompt.strip()}\n\n{content}"
        mime_type = "text/markdown"
        extension = "md"

    elif file_format == "JSON":
        import json

        export_data = {
            "model": model,
            "system_prompt": system_prompt.strip(),
            "messages": st.session_state.messages,
        }
        full_export = json.dumps(export_data, indent=2)
        mime_type = "application/json"
        extension = "json"

    else:
        full_export = "Unsupported format."
        mime_type = "text/plain"
        extension = "txt"
else:
    full_export = "No messages yet."
    mime_type = "text/plain"
    extension = "txt"

timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M")
filename_base = f"chat_{model}_{timestamp}"


# ✅ Always render after messages have been populated
st.sidebar.download_button(
    label=f"Download Chat ({file_format})",
    data=full_export,
    file_name=f"{filename_base}.{extension}",
    mime=mime_type,
)


st.sidebar.markdown("---")
st.sidebar.markdown("🧹 **Delete Chat**")

# 🧹 Clear chat button in sidebar
if st.sidebar.button("Clear Chat"):
    st.session_state.messages = []
    st.rerun()
