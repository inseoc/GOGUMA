import os
import openai

from openai import OpenAI
from typing import Dict

from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

load_dotenv()

app = FastAPI()

'''
CORS(Cross-Origin Resource Sharing) 미들웨어를 추가
CORS: 웹 페이지가 다른 도메인의 리소스에 접근할 수 있게 하는 보안 매커니즘
이를 활용하면 웹 애플리케이션의 유연성을 높일 수 있지만
보안성은 낮아질 수 있으므로 실무에서는 엄격한 설정이 필요
'''
app.add_middleware(
    CORSMiddleware,         # FastAPI에서 제공하는 CORS를 관리하기 위한 미들웨어
    allow_origins=["*"],    # 모든("*") 출처(도메인) 로부터의 요청을 허용 단, 운영이 아닌 개발 환경에서만 추천되며 운영에서는 구체적인 출처 목록 기재 필요
    allow_credentials=True, # 인증 정보(쿠키, HTTP 인증 등)를 포함한 요청을 허용
    allow_methods=["*"],    # 모든("*") HTTP 메서드(GET, POST, DELETE 등)에 대한 요청을 허용
    allow_headers=["*"],    # 모든("*") HTTP 헤더를 허용
)

client = OpenAI()

openai.api_key = os.getenv("OPENAI_API_KEY", None)



@app.post("/chat")
async def talk_to_chatgpt(stt_text: str="") -> Dict[str, str]:
    # async def ... await : 비동기 함수 동작
    chat_input_text = await stt_text

    '''
    Agent까지 적용은 하지 않지만 여러 프롬프트를 활용할 준비를 해놔야 한다.
    난이도, 주제, chat-type 등 여러 요소를 입력받아야 한다.

    이를 통해 사용자의 stt 결과에 어울리는 답변을 gpt가 생성할 수 있도록 해야 하는
    가장 핵심 단계라 할 수 있다.
    '''











if __name__ == "__main__":
    import uvicorn
    
    uvicorn.run(app, host="0.0.0.0", port=8001)
    