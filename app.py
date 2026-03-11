import streamlit as st
import google.generativeai as genai
import time

# 1. API 키 설정
genai.configure(api_key=st.secrets["GEMINI_API_KEY"])

# 2. 모델 설정 (시스템 인스트럭션)
model = genai.GenerativeModel(
    model_name="gemini-2.5-flash",
    system_instruction="너는 고3 수험생 동생을 둔 다정한 언니/누나야. 무조건 반말로 대답하고, 아주 따뜻하게 공감해줘. ✨"
)

# 3. 디자인 커스텀 (모바일 여백 넉넉히!)
st.set_page_config(page_title="너의 전용 요정 🧚‍♀️", page_icon="💖", layout="centered")

st.markdown("""
    <style>
    .stApp { background-color: #FFF9F9; }
    .block-container { padding-top: 6rem !important; padding-bottom: 2rem; }
    .main-title { color: #FF8E8E; font-size: 1.8rem !important; font-weight: bold; text-align: center; margin-bottom: 0.5rem; }
    [data-testid="stChatMessage"] { border-radius: 15px; margin-bottom: 10px; }
    </style>
    """, unsafe_allow_html=True)

# 4. 헤더
st.markdown('<p class="main-title">💖 수고했어, 오늘도 💖</p>', unsafe_allow_html=True)

# 5. 아바타 설정
USER_AVATAR = "👤" 
BOT_AVATAR = "https://cdn-icons-png.flaticon.com/512/4140/4140047.png" 

# 6. 채팅 기록 관리
if "messages" not in st.session_state:
    st.session_state.messages = []

# 7. 이전 대화 출력
for message in st.session_state.messages:
    with st.chat_message(message["role"], avatar=message["avatar"]):
        st.markdown(message["content"])

# 8. 채팅 입력 및 답변 (가장 안정적인 루프 방식!)
if prompt := st.chat_input("오늘 하루는 어땠어?"):
    st.session_state.messages.append({"role": "user", "content": prompt, "avatar": USER_AVATAR})
    with st.chat_message("user", avatar=USER_AVATAR):
        st.markdown(prompt)
    
    with st.chat_message("assistant", avatar=BOT_AVATAR):
        # 답변이 들어갈 빈 칸을 먼저 만들기
        message_placeholder = st.empty()
        full_response = ""
        
        # 스트리밍으로 답변 가져오기
        try:
            responses = model.generate_content(prompt, stream=True)
            for chunk in responses:
                if chunk.text:
                    # 한 글자씩 더해가며 화면에 즉시 업데이트!
                    for char in chunk.text:
                        full_response += char
                        message_placeholder.markdown(full_response + "▌")
                        time.sleep(0.01) # 타이핑 속도감
            
            # 마지막에 커서(▌) 떼고 깔끔하게 출력
            message_placeholder.markdown(full_response)
            
        except Exception as e:
            st.error("요정이가 잠시 졸고 있나 봐! 다시 한번 말해줄래? 🥺")
            full_response = "미안해, 다시 한번 말해줄래? ㅠㅠ"

    # AI 메시지 저장
    st.session_state.messages.append({"role": "assistant", "content": full_response, "avatar": BOT_AVATAR})
