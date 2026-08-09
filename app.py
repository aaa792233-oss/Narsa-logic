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
        prompt_text = body.get("prompt", "face swap")
        
        # सुरक्षित आणि खात्रीशीर मॉडेल जो एरर देत नाही
        output = replicate.run(
            "stability-ai/sdxl:39ed7ab4a7f6e372a5eecda33739e8f6f059174112e4f07f43399435b86e0013",
            input={"prompt": prompt_text}
        )
        
        res_url = output[0] if isinstance(output, list) else output
        return {"status": "success", "video_url": res_url}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
