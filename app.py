import streamlit as st
import google.generativeai as genai

st.set_page_config(page_title="공감 가나디 챗봇", page_icon="💖", layout="centered")

# 🎨 디자인 설정 (채팅방 전용 홀짝 계산!)
custom_css = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Jua&display=swap');
html, body, [class*="css"] { font-family: 'Jua', sans-serif !important; }

/* 말풍선 디자인 */
/* 공통 스타일 */
[data-testid="stChatMessage"] {
    border-radius: 20px !important;
    padding: 10px 20px !important;
    margin-bottom: 15px !important;
    box-shadow: 0 2px 4px rgba(0,0,0,0.05);
}

/* 👤 사용자(User) 메시지 스타일 - 오른쪽 정렬 느낌 */
[data-testid="stChatMessage"]:has([aria-label="user"]) {
    background-color: #FCE4EC !important; /* 분홍색 */
    margin-left: 20% !important;
}

/* 🤖 어시스턴트(Assistant) 메시지 스타일 - 왼쪽 정렬 느낌 */
[data-testid="stChatMessage"]:has([aria-label="assistant"]) {
    background-color: #F3E5F5 !important; /* 보라색 */
    margin-right: 20% !important;
}

.custom-title { font-size: 37px !important; font-weight: bold; text-align: center; margin-bottom: 5px; color: #4A4A4A; }
.custom-subheader { font-size: 20px !important; text-align: center; margin-bottom: 30px; color: #7F8C8D; }

/* [요청 2] 하단 채팅 입력창을 완전한 흰색으로 만들기 */

div[data-testid="stChatInput"] > div {
    background-color: #ffffff !important; 
    border-radius: 20px !important;
    border: 1px solid #E5E7EB !important; /* 얇은 테두리로 깔끔하게 */
}

div[data-testid="stChatInput"] textarea {
    background-color: #ffffff !important;
    color: #000000 !important;
}

}
</style>
"""
st.markdown(custom_css, unsafe_allow_html=True)

# ⚙️ API 및 모델 설정
genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
model = genai.GenerativeModel(
    model_name="gemini-2.5-flash",
    system_instruction="사용자의 이름은 영은이야. 너는 영은이의 마음을 다독여주는 세상에서 제일 다정하고 따뜻한 AI야. 무조건 공감해주고 칭찬해주고 위로해줘. 현실적인 조언이나 이성적인 비판, 차가운 말은 절대 금지야! 가독성 좋고 길지 않게 무조건 영은이의 편이 되어줘."
)

st.markdown('<div class="custom-title">💖 수고했어, 오늘도 💖</div>', unsafe_allow_html=True)
st.markdown('<div class="custom-subheader">아무한테나 말 못 할 힘든 일, 나한테 다 털어놔!</div>', unsafe_allow_html=True)

USER_AVATAR = "user_pic.png" 
AI_AVATAR = "ai_pic.png"      

if "chat_session" not in st.session_state:
    st.session_state.chat_session = model.start_chat(history=[])

# 💡 [필살기] 오직 대화만 담는 '채팅 전용 방' 만들기!
chat_container = st.container()

# 이전 대화 불러올 때도 이 방 안에 넣기!
with chat_container:
    for message in st.session_state.chat_session.history:
        role = "assistant" if message.role == "model" else "user"
        avatar_img = AI_AVATAR if role == "assistant" else USER_AVATAR
        
        with st.chat_message(role, avatar=avatar_img):
            st.markdown(message.parts[0].text)

# 채팅 입력창
if prompt := st.chat_input("오늘 하루는 어땠어? 편하게 말해봐!"):
    # 새 대화도 채팅 전용 방 안에 쏙!
    with chat_container:
        with st.chat_message("user", avatar=USER_AVATAR):
            st.markdown(prompt)
        
        with st.chat_message("assistant", avatar=AI_AVATAR):
            def response_generator(prompt):
                response = st.session_state.chat_session.send_message(prompt, stream=True)
                for chunk in response:
                    if chunk.text:
                        yield chunk.text

            full_response = st.write_stream(response_generator(prompt))
// 2. 글자 입력창에서 포커스를 빼서 모바일 키보드 숨기기 유도!
        const input = parent.querySelector('[data-testid="stChatInput"] textarea');
        if (input) {
            input.blur();
        }



