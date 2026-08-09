from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import replicate
import os
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

os.environ["REPLICATE_API_TOKEN"] = "तुमची_REPLICATE_API_KEY_येथे_टाका"

class VideoRequest(BaseModel):
    prompt: str

@app.post("/api/generate-video")
async def generate_video(request: VideoRequest):
    try:
        # ASCII एरर पूर्णपणे रोखण्यासाठी युनिकोड सुरक्षित करणे
        safe_prompt = request.prompt.encode('ascii', 'ignore').decode('ascii')
        if not safe_prompt.strip():
            safe_prompt = "Cinematic video generation"

        output = replicate.run(
            "lucataco/hotshot-xl:78b3a6257e16e4b241245d65c8b2b81ea2e1ff7ed4c55238b91dc3fa2baaf100",
            input={"prompt": safe_prompt}
        )
        return {"status": "success", "video_url": output}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
