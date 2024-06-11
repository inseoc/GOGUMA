from io import BytesIO
from fastapi import FastAPI, UploadFile, File
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from app.openai_helper import openaiHelper

app = FastAPI()
openai_helper = openaiHelper()

class AudioResponse(BaseModel):
    text: str
    
class TextRequest(BaseModel):
    text: str

class TextResponse(BaseModel):
    response: str
    
    
@app.post("/speech_to_text/", response_model=AudioResponse)
async def speech_to_text(file: UploadFile = File(...)):
    audio_data = await file.read()
    stt_response = openai_helper.stt(audio_data)
    
    return AudioResponse(text=stt_response)


@app.post("/text_to_speech/")
async def text_to_speech(request: TextRequest):
    tts_response = openai_helper.tts(request.text)
    
    # return tts_response
    return StreamingResponse(BytesIO(tts_response), media_type="audio/wav")


@app.post("/gpt_generation/", response_model=TextResponse)
async def gpt_generation(request: TextRequest):
    gpt_response = openai_helper.chat(request.text)
    
    return TextResponse(text=gpt_response)



if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)