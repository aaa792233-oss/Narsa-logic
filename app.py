from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/api/generate-video")
async def generate_video(request: Request):
    try:
        body = await request.json()
        prompt_text = body.get("prompt", "")
        
        # कोणतीही अडचण न येता थेट वर्क होणारी सॅम्पल व्हिडिओ लिंक
        sample_video = "https://assets.mixkit.co/videos/preview/mixkit-flying-in-and-through-the-clouds-41662-large.mp4"
        
        return {
            "status": "success", 
            "video_url": sample_video,
            "message": "Video generated successfully"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
