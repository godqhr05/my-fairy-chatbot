import streamlit as st
import google.generativeai as genai

# 1. API 키 설정
genai.configure(api_key=st.secrets["GEMINI_API_KEY"])

# 2. 모델 설정 (시스템 인스트럭션 포함)
model = genai.GenerativeModel(
    model_name="gemini-2.5-flash",
    system_instruction="너는 고3 수험생 동생을 둔 세상에서 제일 다정한 언니/누나야. 무조건 동생 편에서 공감해주고 따뜻하게 안아줘. 말투는 아주 친근하게 반말로 해줘. ✨"
)

# 3. 디자인 커스텀 (모바일 최적화)
st.set_page_config(page_title="너의 전용 요정", page_icon="💖", layout="centered")

st.markdown("""
    <style>
    .stApp { background-color: #FFF9F9; }
    .block-container { padding-top: 5rem !important; padding-bottom: 2rem; }
    .main-title { color: #FF8E8E; font-size: 1.8rem !important; font-weight: bold; text-align: center; margin-bottom: 0.5rem; }
    [data-testid="stChatMessage"] { border-radius: 15px; margin-bottom: 10px; }
    </style>
    """, unsafe_allow_html=True)

# 4. 헤더
st.markdown('<p class="main-title">💖 수고했어, 오늘도 💖</p>', unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #999; font-size: 0.9rem;'>오늘 하루도 고생 많았어, 내 동생! ✨</p>", unsafe_allow_html=True)

# 5. 아바타 설정
USER_AVATAR = "👤" 
BOT_AVATAR = "https://cdn-icons-png.flaticon.com/512/4140/4140047.png" 

# 6. 채팅 기록 세션 초기화
if "messages" not in st.session_state:
    st.session_state.messages = []

# 7. 이전 대화 기록 출력
for message in st.session_state.messages:
    with st.chat_message(message["role"], avatar=message["avatar"]):
        st.markdown(message["content"])

# 8. 채팅 입력 및 답변 (Streaming 방식 적용!)
if prompt := st.chat_input("오늘 하루는 어땠어?"):
    # 사용자 메시지 표시 및 저장
    st.session_state.messages.append({"role": "user", "content": prompt, "avatar": USER_AVATAR})
    with st.chat_message("user", avatar=USER_AVATAR):
        st.markdown(prompt)
    
    # AI 답변 생성 및 표시 (스트리밍!)
    with st.chat_message("assistant", avatar=BOT_AVATAR):
        # 💡 여기가 핵심! stream=True를 써서 데이터가 오는 대로 바로바로 뿌려줘!
        response = model.generate_content(prompt, stream=True)
        
        # 스트림릿 전용 스트리밍 출력 함수 (폰에서 제일 안정적이야!)
        full_response = st.write_stream(response)
    
    # AI 메시지 저장
    st.session_state.messages.append({"role": "assistant", "content": full_response, "avatar": BOT_AVATAR})
