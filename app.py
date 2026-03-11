import streamlit as st
import google.generativeai as genai

# 1. API 키 설정 (비밀 금고)
genai.configure(api_key=st.secrets["GEMINI_API_KEY"])

# 2. 모델 설정
model = genai.GenerativeModel(
    model_name="gemini-2.5-flash",
    system_instruction="너는 고3 수험생 동생을 둔 다정한 언니/누나야. 무조건 반말로 대답하고, 동생의 고민에 깊이 공감해주고 따뜻하게 위로해줘. ✨"
)

# 3. 디자인 (모바일 최적화 & 깔끔함)
st.set_page_config(page_title="너의 전용 요정 🧚‍♀️", page_icon="💖", layout="centered")

st.markdown("""
    <style>
    .stApp { background-color: #FFF9F9; }
    /* 위쪽 여백 넉넉하게! */
    .block-container { padding-top: 6rem !important; padding-bottom: 2rem; }
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

# 6. 채팅 기록 세션
if "messages" not in st.session_state:
    st.session_state.messages = []

# 7. 이전 대화 기록 출력
for message in st.session_state.messages:
    with st.chat_message(message["role"], avatar=message["avatar"]):
        st.markdown(message["content"])

# 8. 채팅 입력 및 답변 (안정성 1순위 방식!)
if prompt := st.chat_input("오늘 하루는 어땠어?"):
    # 내 메시지 표시
    st.session_state.messages.append({"role": "user", "content": prompt, "avatar": USER_AVATAR})
    with st.chat_message("user", avatar=USER_AVATAR):
        st.markdown(prompt)
    
    # AI 답변 (가장 심플하고 강력한 방식)
    with st.chat_message("assistant", avatar=BOT_AVATAR):
        # 뱅글뱅글 돌아가는 '생각 중' 표시! 폰에서도 "아, 일하고 있구나" 하고 알 수 있어.
        with st.spinner("요정이가 생각 중... 💭"):
            try:
                # 스트리밍 없이 한 번에 가져오기 (모바일 연결 끊김 방지!)
                response = model.generate_content(prompt)
                full_response = response.text
                st.markdown(full_response)
            except Exception as e:
                full_response = "미안해 동생아, 잠시 요정이가 졸았나 봐! 다시 한번 말해줄래? 🥺"
                st.error(full_response)
    
    # 대화 저장
    st.session_state.messages.append({"role": "assistant", "content": full_response, "avatar": BOT_AVATAR})
