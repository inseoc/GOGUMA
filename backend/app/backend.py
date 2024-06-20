from io import BytesIO
from fastapi import FastAPI, UploadFile, File
from fastapi.responses import StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Any
from openai_helper import openaiHelper

app = FastAPI()

# CORS 설정 추가
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],    # 모든 도메인 허용
    allow_credentials=True,
    allow_methods=["*"],    # 모든 HTTP 메서드 허용
    allow_headers=["*"],    # 모든 HTTP 헤더 허용
)


openai_helper = openaiHelper()

class AudioResponse(BaseModel):
    text: str
    
class PersonaRequest(BaseModel):
    gender: str
    persona: str

class TextRequest(BaseModel):
    text: str

class Response(BaseModel):
    status: int
    response: str
    result: Any


@app.post("/setting_for_persona", response_model=Response)
async def setting_for_persona(request: PersonaRequest):
    persona_response = openai_helper.set_persona(request.model_dump())
        
    return Response(**persona_response)

    
@app.post("/speech_to_text", response_model=AudioResponse)
async def speech_to_text(file: UploadFile = File(...)):
    audio_data = await file.read()
    stt_response = openai_helper.stt(audio_data)
    
    return AudioResponse(text=stt_response)


@app.post("/text_to_speech")
async def text_to_speech(request: TextRequest):
    tts_response = openai_helper.tts(request.text)
    
    # return tts_response
    return StreamingResponse(BytesIO(tts_response), media_type="audio/wav")


@app.post("/gpt_generation", response_model=Response)
async def gpt_generation(request: TextRequest):
    gpt_response = openai_helper.chat(request.text)
    
    return Response(**gpt_response)


@app.post("/check_msg/", response_model=Response)
async def check_msg():
    check_response = openai_helper.check_msg()
    
    return Response(**check_response)




if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)