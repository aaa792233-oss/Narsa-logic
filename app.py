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

class ProcessRequest(BaseModel):
    prompt: str
    video_data: str = None
    image_data: str = None

@app.post("/api/generate-video")
async def generate_video(request: ProcessRequest):
    try:
        # Replicate फेस स्वॅप / व्हिडिओ मॉडेल
        output = replicate.run(
            "fofr/face-swap:43eaebfaef93e3d36d4d673199d63897d21b3697e18987b22f6797175782782e",
            input={
                "prompt": request.prompt if request.prompt else "face swap"
            }
        )
        return {"status": "success", "video_url": output}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
