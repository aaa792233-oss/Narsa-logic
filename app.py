from fastapi import FastAPI, HTTPException, Request
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

os.environ["REPLICATE_API_TOKEN"] = "R8_FvEN86Az3fKQZJ2xfH0M3w9JmexZuq21XMoap"

@app.post("/api/generate-video")
async def generate_video(request: Request):
    try:
        body = await request.json()
        prompt_text = body.get("prompt", "cinematic landscape")
        
        # स्टेबल व्हिडिओ डिम्युशनसाठी वेगळे आणि सुलभ मॉडेल
        output = replicate.run(
            "stability-ai/stable-video-diffusion:3f0457b4619da561237f5d5b8f95152af9200924bfac2de8abfa2d03a743b946",
            input={
                "input_image": "https://replicate.delivery/pbxt/JSpW7pWv7L2P8b3g5m9J2X7J8/output.png",
                "fps": 6,
                "motion_bucket_id": 127
            }
        )
        return {"status": "success", "video_url": output[0] if isinstance(output, list) else output}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
