import streamlit as st
import google.generativeai as genai

# 1. API 키 설정 (비밀 금고에서 가져오기)
genai.configure(api_key=st.secrets["GEMINI_API_KEY"])

# 2. 모델 설정
model = genai.GenerativeModel(
    model_name="gemini-2.5-flash",
    system_instruction="너는 고3 수험생 동생을 둔 세상에서 제일 다정한 언니/누나야. 무조건 동생 편에서 공감해주고, 따뜻하게 안아주는 말을 해줘. 현실적인 조언보다는 감정적인 위로가 1순위야! 말투는 아주 친근하게 반말로 해줘. ✨"
)

# 3. 디자인 커스텀 (CSS 마법 가루 🪄)
st.set_page_config(page_title="너의 전용 요정", page_icon="💖")

st.markdown("""
    <style>
    /* 전체 배경색 바꾸기 */
    .stApp {
        background-color: #FFF5F5; /* 연한 핑크빛 배경 */
    }
    
    /* 제목 스타일 */
    h1 {
        color: #FF8E8E !important;
        font-family: 'Nanum Gothic', sans-serif;
        text-align: center;
    }
    
    /* 채팅창 말풍선 둥글게 만들기 */
    [data-testid="stChatMessage"] {
        background-color: white;
        border-radius: 20px;
        box-shadow: 2px 2px 10px rgba(0,0,0,0.05);
        margin-bottom: 10px;
    }
    </style>
    """, unsafe_allow_html=True)

# 4. 헤더 부분
st.title("💖 수고했어 💖\n오늘도")
st.markdown("<p style='text-align: center; color: #888;'>오늘 하루도 버티느라 고생 많았어.\n힘든 일 있으면 나한테 다 말해줘!</p>", unsafe_allow_html=True)

# 5. 대화 기록 관리
if "chat_session" not in st.session_state:
    st.session_state.chat_session = model.start_chat(history=[])

# 이전 대화 출력
for message in st.session_state.chat_session.history:
    role = "assistant" if message.role == "model" else "user"
    with st.chat_message(role):
        st.markdown(message.parts[0].text)

# 6. 채팅 입력창
if prompt := st.chat_input("하고 싶은 말이 뭐야?"):
    with st.chat_message("user"):
        st.markdown(prompt)
    
    with st.chat_message("assistant"):
        response = st.session_state.chat_session.send_message(prompt)
        st.markdown(response.text)



