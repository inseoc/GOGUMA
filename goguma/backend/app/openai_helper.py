import os
from load_dotenv import load_dotenv
from openai import OpenAI
from prompt import PERSONA_PROMPT

load_dotenv()

class openaiHelper:
    
    def __init__(self):
        
        api_key = os.getenv("OPENAI_API_KEY")
        self.chat_model_name = os.getenv("OPENAI_CHAT_MODEL_NAME")
        self.tts_model_name = os.getenv("OPENAI_TTS_MODEL_NAME")
        self.stt_model_name = os.getenv("OPENAI_STT_MODEL_NAME")
        
        self.temperature = 0.5
        self.messages = []
    
        try:
            self.client = OpenAI(api_key=api_key)
        except Exception as e:
            print(e)
        finally:
            print("Client Generated!")
        

    def make_msg(self, _type:str="user", text:str="") -> list:
        
        openai_msg = {"role": _type, "content": text}
        self.messages.append(openai_msg)
        

    def set_temperature(self, temperature):
        self.temperature = temperature
    

    def set_persona(self, request:dict):
        
        age = request["age"]
        gender = request["gender"]
        persona = request["persona"]

        PERSONA_PROMPT = PERSONA_PROMPT.format(age, gender, persona)
        self.make_msg("system", PERSONA_PROMPT)
        

    def chat(self, message) -> dict:
        '''
        유저로부터 텍스트 데이터를 받아 이를 텍스트로 변환하는 함수
        유저로부터 원하는 연령, 성별, 페르소나를 확인 후 이에 맞는 역할을 GPT에게 지정
        역할에 어울리는 대화가 진행되도록 프롬프팅
        
        stream=True로 두어 실시간으로 청크 단위 답변 가능케
        
        사용 모델: gpt-4o
        '''
        
        llm_reply = {"status": 200, "response": ""}
        
        self.make_msg(message)
        
        try:
            completion = self.client.chat.completions.create(
                model=self.chat_model_name,
                messages=self.messages,
                temperature=self.temperature,
                stream=True,
            )
            
            reply = completion.choices[0].message.content
            self.make_msg("assistant", reply)
            llm_reply["response"] = reply
        
        except Exception as e:
            err_msg = f"'chat' function of 'openaiHelper' got the error: {e}"
            llm_reply["response"] = err_msg
            llm_reply["status"] = 401
            
            raise err_msg
        
        finally:
            return llm_reply
        
        
    def tts(self, message) -> dict:
        '''
        GPT로부터 텍스트 데이터를 받아 이를 음성 데이터로 변환하는 함수
        유저가 지정한 성별에 맞춰 alloy, nova로 변경이 가능
        
        
        사용 모델: tts-1
        '''
        
        llm_reply = {"status": 200, "response": ""}

        try:
            speech = self.client.audio.speech.create(
                model=self.tts_model_name,
                voice="alloy", # 'alloy' is man, 'nova' is woman
                input=message,
            )
            
            llm_reply["response"] = speech  # completion.iter_bytes 함수 활용 필요
        
        except Exception as e:
            err_msg = f"'tts' function of 'openaiHelper' got the error: {e}"
            llm_reply["response"] = err_msg
            llm_reply["status"] = 401
            
            raise err_msg
        
        finally:
            return llm_reply
        
        
    def stt(self, message) -> dict:
        '''
        유저로부터 음성 데이터를 받아 이를 텍스트로 변환하는 함수
        저장된 음성 파일 경로를 입력값으로 받아야 하지만 stream 데이터로 처리하고 싶으므로 추후 개발 예정
        
        사용 모델: whisper-1
        '''
        
        llm_reply = {"status": 200, "response": ""}

        try:
            transcriptions = self.client.audio.transcriptions.create(
                model=self.stt_model_name,
            )
            
            llm_reply["response"] = transcriptions
        
        except Exception as e:
            err_msg = f"'stt' function of 'openaiHelper' got the error: {e}"
            llm_reply["response"] = err_msg
            llm_reply["status"] = 401
            
            raise err_msg
        
        finally:
            return llm_reply