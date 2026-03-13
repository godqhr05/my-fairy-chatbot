import streamlit as st
import google.generativeai as genai

st.set_page_config(page_title="공감 요정 챗봇", page_icon="💖", layout="centered")

# [수정 1 & 2] 타이틀 폰트 크기 조정 및 입력창 흰색 배경 CSS 추가
custom_css = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Jua&display=swap');

html, body, [class*="css"] {
    font-family: 'Jua', sans-serif !important;
}

/* 말풍선 디자인 */
[data-testid="stChatMessage"] {
    border-radius: 20px !important;
    padding: 10px 20px !important;
    margin-bottom: 15px !important;
    box-shadow: 0 2px 4px rgba(0,0,0,0.05);
}
[data-testid="stChatMessage"]:nth-child(odd) {
    background-color: #FCE4EC !important;
}
[data-testid="stChatMessage"]:nth-child(even) {
    background-color: #F3E5F5 !important;
}

/* [요청 1] 타이틀과 서브헤더 폰트 크기 맘대로 조절하기 */
.custom-title {
    font-size: 37px !important; /* 메인 제목 크기 (숫자를 키우면 커짐) */
    font-weight: bold;
    text-align: center;
    margin-bottom: 5px;
    color: #4A4A4A;
}
.custom-subheader {
    font-size: 20px !important; /* 부제목 크기 (숫자를 줄이면 작아짐) */
    text-align: center;
    margin-bottom: 30px;
    color: #7F8C8D;
}

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
</style>
"""
st.markdown(custom_css, unsafe_allow_html=True)

genai.configure(api_key=st.secrets["GEMINI_API_KEY"])

model = genai.GenerativeModel(
    model_name="gemini-2.5-flash",
    system_instruction="사용자의 이름은 영은이야. 너는 영은이의 마음을 다독여주는 세상에서 제일 다정하고 따뜻한 AI야. 무조건 공감해주고 칭찬해주고 위로해줘. 현실적인 조언이나 이성적인 비판, 차가운 말은 절대 금지야! 무조건 영은이의 편이 되어줘."
)

# [요청 1 적용] st.title 대신 커스텀 클래스를 써서 크기 조절
st.markdown('<div class="custom-title">💖 수고했어, 오늘도 💖</div>', unsafe_allow_html=True)
st.markdown('<div class="custom-subheader">아무한테나 말 못 할 힘든 일, 나한테 다 털어놔!</div>', unsafe_allow_html=True)

USER_AVATAR = "user_pic.png" 
AI_AVATAR = "ai_pic.png"     

# [요청 3] 대화 기억하기: 'chat_session' 자체가 이전 대화를 계속 누적해서 기억하는 객체야!
if "chat_session" not in st.session_state:
    st.session_state.chat_session = model.start_chat(history=[])

for message in st.session_state.chat_session.history:
    role = "assistant" if message.role == "model" else "user"
    avatar_img = AI_AVATAR if role == "assistant" else USER_AVATAR
    
    with st.chat_message(role, avatar=avatar_img):
        st.markdown(message.parts[0].text)

if prompt := st.chat_input("오늘 하루는 어땠어? 편하게 말해봐!"):
    with st.chat_message("user", avatar=USER_AVATAR):
        st.markdown(prompt)
    
    with st.chat_message("assistant", avatar=AI_AVATAR):
        # 여기서 send_message를 할 때, 이전 대화 내용(history)까지 알아서 같이 전달돼서 맥락을 이해하고 답변해 줌!
        response = st.session_state.chat_session.send_message(prompt)
        st.markdown(response.text)

# 1. 텍스트만 쏙쏙 뽑아주는 '생성기(Generator)'를 만들어
def response_generator(prompt):
    # stream=True 옵션을 줘야 답변이 조각조각 나눠서 와!
    response = model.generate_content(prompt, stream=True)
    for chunk in response:
        if chunk.text:
            yield chunk.text  # 글자 조각을 하나씩 던져줌!

# 2. 채팅창에서 실행할 때
with st.chat_message("assistant", avatar="🧚‍♀️"):
    # st.write_stream이 받은 글자 조각들을 타이핑하듯 보여줘
    full_response = st.write_stream(response_generator(prompt))



