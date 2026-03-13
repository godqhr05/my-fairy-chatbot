import streamlit as st
import google.generativeai as genai
import streamlit.components.v1 as components

st.set_page_config(page_title="공감 요정 챗봇", page_icon="💖", layout="centered")

# [디자인] CSS 설정
custom_css = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Jua&display=swap');
html, body, [class*="css"] { font-family: 'Jua', sans-serif !important; }

/* 말풍선 디자인 */
[data-testid="stChatMessage"] {
    border-radius: 20px !important;
    padding: 10px 20px !important;
    margin-bottom: 15px !important;
    box-shadow: 0 2px 4px rgba(0,0,0,0.05);
}
[data-testid="stChatMessage"]:nth-child(odd) { background-color: #FCE4EC !important; }
[data-testid="stChatMessage"]:nth-child(even) { background-color: #F3E5F5 !important; }

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

# API 설정
genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
model = genai.GenerativeModel(
    model_name="gemini-2.5-flash",
    system_instruction="사용자의 이름은 영은이야. 너는 영은이의 마음을 다독여주는 세상에서 제일 다정하고 따뜻한 AI야. 무조건 공감해주고 칭찬해주고 위로해줘. 현실적인 조언이나 이성적인 비판은 절대 금지! 가독성 좋고 길지 않게 무조건 영은이 편이 되어줘. ✨"
)

# 타이틀 출력
st.markdown('<div class="custom-title">💖 수고했어, 오늘도 💖</div>', unsafe_allow_html=True)
st.markdown('<div class="custom-subheader">아무한테나 말 못 할 힘든 일, 나한테 다 털어놔!</div>', unsafe_allow_html=True)

# 아바타 설정 (파일명 혹은 이모지)
USER_AVATAR = "user_pic.png" 
AI_AVATAR = "ai_pic.png" 

# 대화 세션 관리
if "chat_session" not in st.session_state:
    st.session_state.chat_session = model.start_chat(history=[])

# 이전 대화 기록 출력
for message in st.session_state.chat_session.history:
    role = "assistant" if message.role == "model" else "user"
    avatar_img = AI_AVATAR if role == "assistant" else USER_AVATAR
    with st.chat_message(role, avatar=avatar_img):
        st.markdown(message.parts[0].text)

# 채팅 입력창
if prompt := st.chat_input("오늘 하루는 어땠어? 편하게 말해봐!"):
    # 1. 사용자 메시지 출력
    with st.chat_message("user", avatar=USER_AVATAR):
        st.markdown(prompt)
    
    # 2. AI 답변 생성 및 타이핑 효과 출력
    with st.chat_message("assistant", avatar=AI_AVATAR):
        # 💡 [핵심] 텍스트 조각을 모으는 생성기 함수
        def stream_generator():
            # chat_session을 통해 스트리밍 방식으로 메시지 전송
            response = st.session_state.chat_session.send_message(prompt, stream=True)
            for chunk in response:
                if chunk.text:
                    yield chunk.text

        # st.write_stream이 한 글자씩 써주면서 기록도 합쳐줌!
        full_response = st.write_stream(stream_generator())
# ---------------------------------------------------------
# [꼼수 마법] 화면 맨 아래로 스크롤 & 키보드 내리기 시도!
# ---------------------------------------------------------
components.html(
    """
    <script>
        const parent = window.parent.document;
        
        // 1. 채팅창 스크롤을 맨 밑으로 쫙! 끌어내리기
        const main = parent.querySelector('.main');
        if (main) {
            main.scrollTo(0, main.scrollHeight);
        }

    </script>
    """,
    height=0
)




