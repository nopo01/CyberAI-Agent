import streamlit as st
from duckduckgo_search import DDGS

st.set_page_config(page_title="CyberAI Search", page_icon="🔍")
st.title("🔍 CyberAI Search | محرك البحث السيبراني الحي")
st.caption("بحث مباشر في أدوات Kali Linux، الثغرات، والأوامر الأمنية بدون ذكاء اصطناعي.")

if "messages" not in st.session_state:
    st.session_state["messages"] = [{"role": "assistant", "content": "مرحباً بك يا CEO! أدخل اسم الأداة، الثغرة، أو الأمر لجلب أحدث نتائج البحث المباشرة من الإنترنت."}]

for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

if prompt := st.chat_input("ابحث عن أمر، ثغرة، أو أداة أمنية..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user").write(prompt)

    with st.spinner("جاري جلب النتائج الحية من شبكة الإنترنت..."):
        try:
            with DDGS() as ddgs:
                # يقتصر البحث على المواقع والمصادر السيبرانية
                query = f"{prompt} cybersecurity kali linux documentation"
                results = list(ddgs.text(query, max_results=5))
                
                if results:
                    response = "### 🌐 أهم نتائج البحث الحية المباشرة:\n\n"
                    for i, r in enumerate(results, 1):
                        response += f"**{i}. [{r['title']}]({r['href']})**\n"
                        response += f"{r['body']}\n\n---\n"
                else:
                    response = "❌ لم يتم العثور على نتائج حية متعلقة ببحثك، جرب كتابة اسم الأداة أو الأمر بالإنجليزية."
        except Exception as e:
            response = f"⚠️ حدث خطأ أثناء الاتصال بالإنترنت: {str(e)}"

    st.session_state.messages.append({"role": "assistant", "content": response})
    st.chat_message("assistant").write(response)
