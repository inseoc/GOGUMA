import json
import requests
import streamlit as st

STT_API_URL="http://localhost:8001/stt"
CHAT_API_URL="http://localhost:8001/chat"
TTS_API_URL="http://localhost:8001/tts"

def init_session_state():
    '''
    초기 session_state 설정
    '''
    if "stt_source" not in st.session_state:
        st.session_state["stt_source"] = ""

    if "chat_source" not in st.session_state:
        st.session_state["chat_source"] = ""

    if "tts_source" not in st.session_state:
        st.session_state["tts_source"] = ""

    if "talk_type" not in st.session_state:
        st.session_state["talk_type"] = ""

    if "full_chat" not in st.session_state:
        st.session_state["full_chat"] = ""

    if "role_playing" not in st.session_state:
        st.session_state["role_playing"] = ""

    if "jargon" not in st.session_state:
        st.session_state["jargon"] = ""


def stt_result_ui(uploaded_file=None):
    '''
    stt 결과를 텍스트로 제공
    '''
    stt_done = False

    files = {"file": uploaded_file}
    response = requests.post(STT_API_URL, files=files)

    try:
        st.write(response.json()["result"])
        st.session_state["stt_source"] = response.json()["result"]
        stt_done = True
    except Exception as e:
        print(e)
        st.write("Error in STT response.")

    finally:
        return stt_done
    

def tts_result_ui():
    '''
    tts 결과를 음성과 텍스트로 동시 제공
    '''
    tts_done = False

    response = requests.post(TTS_API_URL)

    try:
        tts_audio_result = response.json()["result"]
        st.write(tts_audio_result)
        st.session_state["stt_source"] = response.json()["result"]
        tts_done = True

        st.audio(tts_audio_result, format="audio/wav")

    except Exception as e:
        print(e)
        st.write("Error in TTS response.")

    finally:
        return tts_done


def input_ui_1():
    '''
    1. free-talking 을 위한 'full_chat' 버전
    2. 초보자 혹은 전문용어 대화를 위한 'role_playing' 버전
    '''
    st.subheader("Select Talk Type")
    
    talk_types = ["full_chat", "role_playing"]
    talk_type = st.selectbox("Select a type:", talk_types)

    st.session_state["talk_type"] = talk_type


def input_ui_2():
    '''
    만약 role_playing 을 골랐다면, 원하는 주제를 사용자가 직접 입력
    추후 예외 발생을 예방하기 위해 주제 목록을 만들어 두는 것이 좋을 듯
    '''
    st.subheader("Select Subject")

    subject_name = st.text_input("Input subject")

    if st.button("Click"):
        st.session_state["jargon"] = subject_name


def main():

    st.title("○ Setting ○")

    init_session_state()
    
    stt_done_flag = False

    try:
        uploaded_file = st.file_uploader("Upload audio file", type=["mp3", "mp4", "wav"])
    except Exception as e:
        uploaded_file = None
        st.write(f"Your file type is not in ['mp3', 'mp4', 'wav'] | Error mag: {e}")

    if uploaded_file is not None:
        stt_done_flag = stt_result_ui(uploaded_file)

    col1, col2 = st.columns(2)

    with col1:
        input_ui_1()

    if st.session_state["talk_type"] == "role_playing":
        with col2:
            input_ui_2()


    st.title("o GPT's Speak o")
    # 24.1.3 개발 이어서..
    # if stt_done_flag:
    #     tts_result_ui()


if __name__ == "__main__":
    st.set_page_config(layout="wide")
    st.header("◎ TALKTO ◎")

    main()

