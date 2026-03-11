import streamlit as st
import google.generativeai as genai

# [요청 4] 모바일 최적화: 화면을 모바일에 맞게 가운데 정렬 (반드시 코드 최상단에 위치해야 해!)
st.set_page_config(page_title="공감 요정 챗봇", page_icon="💖", layout="centered")

# [요청 3] 말풍선 둥글게, 귀여운 폰트(구글 폰트 Jua), 테마 컬러 CSS 적용
custom_css = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Jua&display=swap');

/* 전체 폰트 귀엽게 변경 */
html, body, [class*="css"] {
    font-family: 'Jua', sans-serif !important;
}

/* 채팅 메시지 말풍선을 둥글게 만들기 */
[data-testid="stChatMessage"] {
    border-radius: 20px !important;
    padding: 10px 20px !important;
    margin-bottom: 15px !important;
    box-shadow: 0 2px 4px rgba(0,0,0,0.05);
}

/* User (동생) 말풍선 스타일 - 연한 핑크 */
[data-testid="stChatMessage"]:nth-child(odd) {
    background-color: #FCE4EC !important;
}

/* Assistant (AI) 말풍선 스타일 - 연한 보라 */
[data-testid="stChatMessage"]:nth-child(even) {
    background-color: #F3E5F5 !important;
}
</style>
"""
# CSS 적용시키기
st.markdown(custom_css, unsafe_allow_html=True)

# 1. API 키 설정
genai.configure(api_key=st.secrets["GEMINI_API_KEY"])

# 2. 모델 설정 (F 성향 100% 공감 요정 페르소나 주입! 🧚‍♀️)
model = genai.GenerativeModel(
    model_name="gemini-2.5-flash",
    system_instruction="너는 수험생의 마음을 다독여주는 세상에서 제일 다정하고 따뜻한 AI야. 무조건 공감해주고 칭찬해줘. 현실적인 조언이나 이성적인 비판, 차가운 말은 절대 금지야! 무조건 내 편이 되어줘."
)

# 3. 웹페이지 화면 꾸미기 🎨
st.title("💖 수고했어 오늘도 💖")
st.subheader("아무한테나 말 못 할 힘든 일, 나한테 다 털어놔!")

# [요청 1] 맞춤형 프로필 이미지 이름 설정
# ⚠️ 깃허브(로컬)의 이 파이썬 파일이 있는 곳과 '같은 폴더'에 이미지 파일 2개를 꼭 넣어줘!
USER_AVATAR = "user_pic.png"  # 동생 프로필 사진
AI_AVATAR = "ai_pic.png"      # AI 공감 요정 프로필 사진

# 4. 대화 기록 저장하는 마법의 주머니
# [요청 5] 대화 기억하기: Gemini의 start_chat 기능이 이미 완벽하게 과거 대화를 기억해 주고 있어!
if "chat_session" not in st.session_state:
    st.session_state.chat_session = model.start_chat(history=[])

# 이전 대화 내용들 화면에 띄워주기 (아바타 이미지 추가 적용)
for message in st.session_state.chat_session.history:
    role = "assistant" if message.role == "model" else "user"
    avatar_img = AI_AVATAR if role == "assistant" else USER_AVATAR # 역할에 맞는 사진 배정
    
    with st.chat_message(role, avatar=avatar_img):
        st.markdown(message.parts[0].text)

# 5. 채팅 입력창 만들기 💬
if prompt := st.chat_input("오늘 하루는 어땠어? 편하게 말해봐!"):
    
    # 내가 쓴 말 화면에 띄우기 (동생 프로필 사진 적용)
    with st.chat_message("user", avatar=USER_AVATAR):
        st.markdown(prompt)
    
    # AI의 따뜻한 답변 받아오기! (AI 프로필 사진 적용)
    with st.chat_message("assistant", avatar=AI_AVATAR):
        # Gemini가 알아서 이전 대화(문맥)를 다 기억하고 답변을 만들어줘!
        response = st.session_state.chat_session.send_message(prompt)
        st.markdown(response.text)
