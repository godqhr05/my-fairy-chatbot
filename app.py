import streamlit as st
import google.generativeai as genai
import time

# 1. API 키 설정 (비밀 금고에서 가져오기)
genai.configure(api_key=st.secrets["GEMINI_API_KEY"])

# 2. 모델 설정
model = genai.GenerativeModel(
    model_name="gemini-2.5-flash",
    system_instruction="너는 고3 수험생 동생을 둔 세상에서 제일 다정한 언니/누나야. 무조건 동생 편에서 공감해주고 따뜻하게 안아줘. 말투는 아주 친근하게 반말로 해줘. ✨"
)

# 3. 디자인 커스텀 (모바일 최적화 & 타이핑 효과 대비 CSS)
st.set_page_config(page_title="너의 전용 요정", page_icon="💖", layout="centered")

st.markdown("""
    <style>
    /* 전체 배경 및 폰트 설정 */
    .stApp {
        background-color: #FFF9F9;
    }
    
    /* 모바일에서 여백 줄이기 */
    .block-container {
        padding-top: 2rem;
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
st.markdown("<p style='text-align: center; color: #999; font-size: 0.9rem;'>동생아, 힘들 땐 언제든 언니한테 말해! ✨</p>", unsafe_allow_html=True)

# 5. 프로필 사진 설정 (인터넷 이미지 링크로 대체 가능!)
# 직접 사진을 쓰고 싶다면 깃허브에 사진 올리고 그 링크를 넣으면 돼!
USER_AVATAR = "👤" # 여기에 이미지 URL 넣으면 사진으로 바뀜!
BOT_AVATAR = "https://cdn-icons-png.flaticon.com/512/4140/4140047.png" # 귀여운 요정 아이콘

# 6. 대화 기록 관리
if "messages" not in st.session_state:
    st.session_state.messages = []

# 이전 대화 출력
for message in st.session_state.messages:
    with st.chat_message(message["role"], avatar=message["avatar"]):
        st.markdown(message["content"])

# 7. 채팅 입력창 및 타이핑 효과
if prompt := st.chat_input("오늘 하루는 어땠어?"):
    # 사용자 메시지 저장 및 출력
    st.session_state.messages.append({"role": "user", "content": prompt, "avatar": USER_AVATAR})
    with st.chat_message("user", avatar=USER_AVATAR):
        st.markdown(prompt)
    
    # AI 답변 생성 및 타이핑 효과
    with st.chat_message("assistant", avatar=BOT_AVATAR):
        message_placeholder = st.empty() # 타이핑 효과를 위한 빈 칸
        full_response = ""
        
        # 모델에게 메시지 보내기
        response = model.generate_content(prompt) # 대화 흐름을 위해 간단하게 구현
        
        # 한 글자씩 출력하는 마법 (타이핑 효과)
        for chunk in response.text:
            full_response += chunk
            time.sleep(0.02) # 타이핑 속도 조절
            message_placeholder.markdown(full_response + "▌")
        
        message_placeholder.markdown(full_response)
    
    # AI 메시지 저장
    st.session_state.messages.append({"role": "assistant", "content": full_response, "avatar": BOT_AVATAR})
