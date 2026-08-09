from fastapi import FastAPI, HTTPException, UploadFile, File, Form
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

@app.post("/api/generate-video")
async def generate_video(
    prompt: str = Form(default=""),
    video: UploadFile = File(default=None),
    image: UploadFile = File(default=None)
):
    try:
        # जर फाईल्स आल्या असतील तर फेस स्वॅप मॉडेल रन करणे
        # (सध्या Replicate साठी URL लागतात, त्यामुळे फाईल्स अपलोडची सुविधा जोडली आहे)
        output = replicate.run(
            "fofr/face-swap:43eaebfaef93e3d36d4d673199d63897d21b3697e18987b22f6797175782782e",
            input={
                "prompt": prompt if prompt else "face swap"
            }
        )
        return {"status": "success", "video_url": output}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
