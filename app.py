import streamlit as st
import google.generativeai as genai
import time

# 1. API 키 설정
genai.configure(api_key=st.secrets["GEMINI_API_KEY"])

# 2. 모델 설정
model = genai.GenerativeModel(
    model_name="gemini-2.5-flash",
    system_instruction="너는 고3 수험생 동생을 둔 세상에서 제일 다정한 언니/누나야. 무조건 동생 편에서 공감해주고 따뜻하게 안아줘. 말투는 아주 친근하게 반말로 해줘. ✨"
)

# 3. 디자인 커스텀 (여백 대폭 수정! 🚀)
st.set_page_config(page_title="너의 전용 요정 🧚‍♀️", page_icon="💖", layout="centered")

st.markdown("""
    <style>
    /* 전체 배경 설정 */
    .stApp {
        background-color: #FFF9F9;
    }
    
    /* ⭐ 상단 잘림 방지: 위쪽 여백을 5rem으로 늘림! */
    .block-container {
        padding-top: 5rem !important; 
        padding-bottom: 2rem;
        padding-left: 1rem;
        padding-right: 1rem;
    }

    /* 제목 스타일 */
    .main-title {
        color: #FF8E8E;
        font-size: 1.8rem !important;
        font-weight: bold;
        text-align: center;
        margin-top: 1rem; /* 제목 위에도 여유 한 번 더! */
        margin-bottom: 0.5rem;
    }

    /* 채팅창 말풍선 디자인 */
    [data-testid="stChatMessage"] {
        border-radius: 15px;
        padding: 10px;
        margin-bottom: 10px;
    }
    </style>
    """, unsafe_allow_html=True)

# 4. 헤더 부분
st.markdown('<p class="main-title">💖 수고했어, 오늘도 💖</p>', unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #999; font-size: 0.9rem;'>오늘 하루도 고생 많았어, 내 동생! ✨</p>", unsafe_allow_html=True)

# 5. 프로필 사진 설정
USER_AVATAR = "👤" 
BOT_AVATAR = "https://cdn-icons-png.flaticon.com/512/4140/4140047.png" 

# 6. 대화 기록 관리
if "messages" not in st.session_state:
    st.session_state.messages = []

# 이전 대화 출력
for message in st.session_state.messages:
    with st.chat_message(message["role"], avatar=message["avatar"]):
        st.markdown(message["content"])

# 7. 채팅 입력창 및 타이핑 효과
if prompt := st.chat_input("오늘 하루는 어땠어?"):
    st.session_state.messages.append({"role": "user", "content": prompt, "avatar": USER_AVATAR})
    with st.chat_message("user", avatar=USER_AVATAR):
        st.markdown(prompt)
    
    with st.chat_message("assistant", avatar=BOT_AVATAR):
        message_placeholder = st.empty()
        full_response = ""
        
        # 모델 답변 생성 (스트리밍 방식 대신 생성 후 타이핑 효과)
        response = model.generate_content(prompt)
        
        # 한 글자씩 출력 (타이핑 효과)
        for chunk in response.text:
            full_response += chunk
            time.sleep(0.01) # 0.02에서 조금 더 빠르게 조절해봤어!
            message_placeholder.markdown(full_response + "▌")
        
        message_placeholder.markdown(full_response)
    
    st.session_state.messages.append({"role": "assistant", "content": full_response, "avatar": BOT_AVATAR})
