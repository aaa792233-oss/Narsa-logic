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

os.environ["REPLICATE_API_TOKEN"] = "तुमची_REPLICATE_API_KEY_येथे_टाका"

@app.post("/api/generate-video")
async def generate_video(request: Request):
    try:
        body = await request.json()
        prompt_text = body.get("prompt", "cinematic video")
        
        output = replicate.run(
            "lucataco/hotshot-xl:78b3a6257e16e4b241245d65c8b2b81ea2e1ff7ed4c55238b91dc3fa2baaf100",
            input={"prompt": prompt_text}
        )
        return {"status": "success", "video_url": output}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
