import streamlit as st
import google.generativeai as genai

# 1. API 키 설정 (비밀 금고)
genai.configure(api_key=st.secrets["GEMINI_API_KEY"])

# 2. 모델 설정
model = genai.GenerativeModel(
    model_name="gemini-2.5-flash",
    system_instruction="너는 고3 수험생 동생을 둔 다정한 언니/누나야. 무조건 반말로 대답하고, 따뜻하게 공감해줘. ✨"
)

# 3. 디자인 커스텀 (모바일 텍스트 시인성 강화!)
st.set_page_config(page_title="너의 전용 요정 🧚‍♀️", page_icon="💖", layout="centered")

st.markdown("""
    <style>
    /* 전체 배경 */
    .stApp {
        background-color: #FFF9F9;
    }
    
    /* 상단 여백 및 기본 텍스트 색상 강제 (다크모드 방지) */
    .block-container {
        padding-top: 6rem !important;
        color: #2D2D2D !important; 
    }

    /* 제목 스타일 */
    .main-title {
        color: #FF8E8E;
        font-size: 1.8rem !important;
        font-weight: bold;
        text-align: center;
        margin-bottom: 0.5rem;
    }

    /* 채팅창 말풍선 내부 텍스트 강제 노출 🪄 */
    [data-testid="stChatMessage"] p, [data-testid="stChatMessage"] span, [data-testid="stChatMessage"] div {
        color: #2D2D2D !important; /* 텍스트 색상을 진하게 고정! */
    }
    
    [data-testid="stChatMessage"] {
        background-color: #FFFFFF !important; /* 말풍선 배경은 하얗게 */
        border-radius: 15px;
        margin-bottom: 10px;
        border: 1px solid #FFEAEA; /* 아주 연한 테두리 추가 */
    }
    </style>
    """, unsafe_allow_html=True)

# 4. 헤더
st.markdown('<p class="main-title">💖 수고했어, 오늘도 💖</p>', unsafe_allow_html=True)

# 5. 프로필 이모지로 깔끔하게 교체! ✨
USER_AVATAR = "👤" 
BOT_AVATAR = "🧚‍♀️" 

# 6. 채팅 기록 관리
if "messages" not in st.session_state:
    st.session_state.messages = []

# 7. 이전 대화 출력
for message in st.session_state.messages:
    with st.chat_message(message["role"], avatar=message["avatar"]):
        st.markdown(message["content"])

# 8. 채팅 입력 및 답변 (안정성 최우선)
if prompt := st.chat_input("오늘 하루는 어땠어?"):
    st.session_state.messages.append({"role": "user", "content": prompt, "avatar": USER_AVATAR})
    with st.chat_message("user", avatar=USER_AVATAR):
        st.markdown(prompt)
    
    with st.chat_message("assistant", avatar=BOT_AVATAR):
        with st.spinner("요정이가 생각 중... 💭"):
            try:
                response = model.generate_content(prompt)
                full_response = response.text
                st.markdown(full_response)
            except:
                full_response = "미안해 동생아, 잠시 통신이 불안정했나 봐! 다시 말해줄래? 🥺"
                st.markdown(full_response)
    
    st.session_state.messages.append({"role": "assistant", "content": full_response, "avatar": BOT_AVATAR})
