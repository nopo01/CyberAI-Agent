import streamlit as st
from duckduckgo_search import DDGS

st.set_page_config(page_title="CyberAI-Agent", page_icon="🛡️")
st.title("🛡️ CyberAI-Agent | الذكاء الاصطناعي للأمن السيبراني")
st.caption("نموذج سيبراني متخصص في Kali Linux والبحث الحي عن الثغرات والأوامر الأمنية.")

if "messages" not in st.session_state:
    st.session_state["messages"] = [{"role": "assistant", "content": "مرحباً بك! أنا مساعدك السيبراني. كيف يمكنني مساعدتك اليوم؟"}]

for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

if prompt := st.chat_input("أدخل سؤالك أو الأمر السيبراني هنا..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user").write(prompt)

    with st.spinner("جاري البحث والتحليل السيبراني..."):
        try:
            with DDGS() as ddgs:
                results = list(ddgs.text(prompt + " kali linux cybersecurity", max_results=3))
                if results:
                    context = "\n".join([f"- **{r['title']}**: {r['body']}" for r in results])
                    search_res = f"🔍 **نتائج البحث الحي:**\n{context}"
                else:
                    search_res = "لم يتم العثور على نتائج خارجية حية."
        except Exception as e:
            search_res = f"حدث خطأ أثناء البحث الحي: {str(e)}"

        response = f"🛡️ **تحليل الذكاء الاصطناعي السيبراني:**\n\nبناءً على طلبك حول: `{prompt}`\n\n{search_res}\n\n⚠️ *تنبيه أمني: استخدم هذه الأوامر والسكربتات في أغراض الفحص المصرح به فقط.*"

    st.session_state.messages.append({"role": "assistant", "content": response})
    st.chat_message("assistant").write(response)