import os

from openai import OpenAI
from typing import Dict

from dotenv import load_dotenv
from fastapi import FastAPI, UploadFile, File
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

@app.post("/stt")
async def upload_audio_and_transcribe(file: UploadFile = File(...)) -> Dict[str, str]:
    # async def ... await : 비동기 함수 동작
    # 'file.file' 속성을 사용하여 'UploadFile'의 파일 콘텐츠에 접근
    # audio_data = file.file
    audio_data = await file.read()

    # 파일을 임시로 저장하고 해당 파일 경로를 사용
    temp_file_path = f"./temp_{file.filename}"
    with open(temp_file_path, "wb") as temp_file:
        temp_file.write(audio_data)
    print(os.path.abspath(temp_file_path))

    # OpenAI의 음성 인식 서비스를 사용하여 텍스트로 변환
    with open(temp_file_path, "rb") as audio_file:
        transcript = client.audio.transcriptions.create(
            model="whisper-1", 
            file=audio_file,  # 파일 객체를 직접 전달
        )

    # 결과 반환
    stt_text = transcript.text

    if isinstance(stt_text, str):
        os.remove(os.path.abspath(temp_file_path))  # 임시 파일 삭제
        return {"result": stt_text}
    else:
        return {"result": f"STT result's type is not string.\nSTT API Result: {stt_text}"}


if __name__ == "__main__":
    import uvicorn
    
    uvicorn.run(app, host="0.0.0.0", port=8001)