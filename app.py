import streamlit as st
import google.generativeai as genai

# 1. API 키 설정 (발급받은 키를 따옴표 안에 넣어줘!)
genai.configure(api_key="api_key=st.secrets['GEMINI_API_KEY']")

# 2. 모델 설정 (F 성향 100% 공감 요정 페르소나 주입! 🧚‍♀️)
model = genai.GenerativeModel(
    model_name="gemini-2.5-flash",
    system_instruction="너는 수험생의 마음을 다독여주는 세상에서 제일 다정하고 따뜻한 AI야. 무조건 공감해주고 칭찬해줘. 현실적인 조언이나 이성적인 비판, 차가운 말은 절대 금지야! 무조건 내 편이 되어줘."
)

# 3. 웹페이지 화면 꾸미기 🎨
st.set_page_config(page_title="공감 요정 챗봇", page_icon="💖")
st.title("💖 수고했어 오늘도 💖")
st.subheader("아무한테나 말 못 할 힘든 일, 나한테 다 털어놔!")

# 4. 대화 기록 저장하는 마법의 주머니
if "chat_session" not in st.session_state:
    st.session_state.chat_session = model.start_chat(history=[])

# 이전 대화 내용들 화면에 띄워주기
for message in st.session_state.chat_session.history:
    role = "assistant" if message.role == "model" else "user"
    with st.chat_message(role):
        st.markdown(message.parts[0].text)

# 5. 채팅 입력창 만들기 💬
if prompt := st.chat_input("오늘 하루는 어땠어? 편하게 말해봐!"):
    
    # 내가 쓴 말 화면에 띄우기
    with st.chat_message("user"):
        st.markdown(prompt)
    
    # AI의 따뜻한 답변 받아오기!
    with st.chat_message("assistant"):
        response = st.session_state.chat_session.send_message(prompt)
        st.markdown(response.text)