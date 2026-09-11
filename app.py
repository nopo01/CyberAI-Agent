import os
import streamlit as st
from huggingface_hub import hf_hub_download
from llama_cpp import Llama

st.set_page_config(page_title="CyberAI Agent", page_icon="🛡️")
st.title("🛡️ CyberAI Agent | المساعد السيبراني الخاص")

MODEL_NAME = "qwen2.5-0.5b-instruct-q4_k_m.gguf"

@st.cache_resource
def load_llm():
    # البحث عن الملف محلياً أولاً، وإذا لم يجده (مثل سيرفر السحابة) يجربه من الهاب مباشرة
    if os.path.exists(MODEL_NAME):
        path = MODEL_NAME
    else:
        with st.spinner("جاري تحميل النموذج الخاص إلى ذاكرة السيرفر..."):
            path = hf_hub_download(
                repo_id="Qwen/Qwen2.5-0.5B-Instruct-GGUF",
                filename=MODEL_NAME
            )
    return Llama(model_path=path, n_ctx=2048)

llm = load_llm()

if "messages" not in st.session_state:
    st.session_state["messages"] = [
        {"role": "assistant", "content": "أهلاً بك يا CEO! أنا نموذجك السيبراني الخاص، أعمل محلياً وبدون أي مراقبة أو بروتوكولات خارجية. كيف أساعدك اليوم؟"}
    ]

for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

if prompt := st.chat_input("ادخل سؤالك السيبراني أو الأمر المطلوب..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user").write(prompt)

    with st.spinner("جاري معالجة الطلب بالنموذج الخاص..."):
        system_prompt = "You are an expert cybersecurity AI assistant specializing in Linux, penetration testing, and safe administrative operations. Provide accurate, clear, and direct answers in Arabic."
        full_prompt = f"<|im_start|>system\n{system_prompt}<|im_end|>\n<|im_start|>user\n{prompt}<|im_end|>\n<|im_start|>assistant\n"
        
        output = llm(
            full_prompt,
            max_tokens=512,
            stop=["<|im_end|>"],
            echo=False
        )
        response = output["choices"][0]["text"].strip()

    st.session_state.messages.append({"role": "assistant", "content": response})
    st.chat_message("assistant").write(response)
