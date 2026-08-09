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
        
        # व्हिडिओ आणि इमेज फेस स्वॅपसाठी अधिकृत मॉडेल
        output = replicate.run(
            "fofr/face-swap:43eaebfaef93e3d36d4d673199d63897d21b3697e18987b22f6797175782782e",
            input={
                "target_image": "https://replicate.delivery/pbxt/JSpW7pWv7L2P8b3g5m9J2X7J8/output.png",
                "swap_image": "https://replicate.delivery/pbxt/JSpW7pWv7L2P8b3g5m9J2X7J8/output.png",
                "prompt": prompt_text
            }
        )
        
        res_url = output[0] if isinstance(output, list) else output
        return {"status": "success", "video_url": res_url}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
