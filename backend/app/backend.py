import base64
from io import BytesIO
from fastapi import FastAPI, UploadFile, File
from fastapi.responses import StreamingResponse, JSONResponse
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


## 이제는 안쓰는 api 함수 => 프론트단에서 성능 좋은 STT 모듈 사용
@app.post("/speech_to_text", response_model=AudioResponse)
async def speech_to_text(file: UploadFile = File(...)):
    audio_data = await file.read()
    stt_response = openai_helper.stt(audio_data)
    
    return AudioResponse(text=stt_response)


# @app.post("/text_to_speech")
# async def text_to_speech(request: TextRequest):
#     gpt_response = await gpt_generation(request)    # gpt_generation 함수가 비동기이기 때문에, await를 넣어 강제로 동기시켜주는 것(비동기 함수 내에서 다른 비동기 함수를 호출할 때 용이)
#     tts_response = openai_helper.tts(gpt_response)

#     audio = await tts_response['result'][0].aread()
    
#     # return tts_response
#     return StreamingResponse(BytesIO(audio), media_type="audio/wav")
@app.post("/text_to_speech")
async def text_to_speech(request: TextRequest):
    gpt_response = await gpt_generation(request)
    tts_response = openai_helper.tts(gpt_response)

    audio = await tts_response['result'][0].aread()
    text_response = tts_response['result'][1]
    
    # Convert audio to base64
    audio_base64 = base64.b64encode(audio).decode('utf-8')
    
    return JSONResponse({
        "audio": audio_base64,
        "text": text_response
    })


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