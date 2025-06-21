from openai import OpenAI
import streamlit as st

import os
import streamlit as st
from openai import OpenAI

# --- 비밀번호 설정 ---
PASSWORD = "0208"

# 인증 상태 저장
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

# 인증이 안 된 경우 로그인 화면만 보여줌
if not st.session_state.authenticated:
    st.title("🔐 다은이의 생일은 언제게~")
    password = st.text_input("숫자 네자리입니다!", type="password")
    if st.button("다은봇 사용하기"):
        if password == PASSWORD:
            st.session_state.authenticated = True
            st.success("정답입니다람쥐!")
            st.rerun()
        else:
            st.error("꺼지세요.")
    st.stop() 
st.title("무엇이든 물어보살🤖")

client = OpenAI()

if "openai_model" not in st.session_state:
    st.session_state["openai_model"] = "gpt-4.1"

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("친절하게 대답해드립니다람쥐"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        stream = client.chat.completions.create(
            model=st.session_state["openai_model"],
            messages=[
                {"role": m["role"], "content": m["content"]}
                for m in st.session_state.messages
            ],
            stream=True,
        )
        response = st.write_stream(stream)
    st.session_state.messages.append({"role": "assistant", "content": response})

