from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import replicate
import os
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

os.environ["REPLICATE_API_TOKEN"] = "तुमची_REPLICATE_API_KEY_येथे_टाका"

class FaceSwapRequest(BaseModel):
    video_url: str
    face_image_url: str

@app.post("/api/generate-video")
async def generate_video(request: FaceSwapRequest):
    try:
        # Replicate वरील फेस स्वॅप (Roop / Face Replacement) मॉडेलला कॉल
        output = replicate.run(
            "fofr/face-swap:43eaebfaef93e3d36d4d673199d63897d21b3697e18987b22f6797175782782e",
            input={
                "target_video": request.video_url,
                "swap_image": request.face_image_url
            }
        )
        return {"status": "success", "video_url": output}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
