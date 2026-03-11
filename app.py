import streamlit as st
import google.generativeai as genai

# 1. API 키 설정
genai.configure(api_key=st.secrets["GEMINI_API_KEY"])

# 2. 모델 설정 (시스템 인스트럭션 보강!)
model = genai.GenerativeModel(
    model_name="gemini-2.5-flash",
    system_instruction="너는 고3 수험생 동생을 둔 다정한 언니/누나야. 무조건 반말로 대답하고, 마크다운 코드 블록(```) 같은 건 절대 쓰지 마. 그냥 사람처럼 다정하게 텍스트로만 말해줘. ✨"
)

# 3. 디자인 커스텀
st.set_page_config(page_title="너의 전용 요정 🧚‍♀️", page_icon="💖", layout="centered")

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

# 5. 아바타 설정
USER_AVATAR = "👤" 
BOT_AVATAR = "[https://cdn-icons-png.flaticon.com/512/4140/4140047.png](https://cdn-icons-png.flaticon.com/512/4140/4140047.png)" 

# 6. 채팅 기록 관리
if "messages" not in st.session_state:
    st.session_state.messages = []

# 7. 이전 대화 출력
for message in st.session_state.messages:
    with st.chat_message(message["role"], avatar=message["avatar"]):
        st.markdown(message["content"])

# 8. 채팅 입력 및 답변 (코드 방지 로직 추가!)
if prompt := st.chat_input("오늘 하루는 어땠어?"):
    st.session_state.messages.append({"role": "user", "content": prompt, "avatar": USER_AVATAR})
    with st.chat_message("user", avatar=USER_AVATAR):
        st.markdown(prompt)
    
    with st.chat_message("assistant", avatar=BOT_AVATAR):
        # 💡 [핵심] 텍스트만 쏙쏙 뽑아주는 생성기 함수!
        def response_generator():
            response = model.generate_content(prompt, stream=True)
            for chunk in response:
                if chunk.text:
                    yield chunk.text

        # 이제 코드가 아니라 '글자'로만 출력될 거야!
        full_response = st.write_stream(response_generator())
    
    st.session_state.messages.append({"role": "assistant", "content": full_response, "avatar": BOT_AVATAR})
