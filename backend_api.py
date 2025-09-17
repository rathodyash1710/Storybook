from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from langchain_huggingface import HuggingFaceEndpoint, ChatHuggingFace
from huggingface_hub import InferenceClient
from dotenv import load_dotenv
from langsmith.run_helpers import traceable
import os, base64
from io import BytesIO
from gtts import gTTS
import tempfile
import re
from typing import Optional


# ----------------------------
# Load env
# ----------------------------
load_dotenv()
HF_TOKEN = os.getenv("HF_TOKEN")
if not HF_TOKEN:
    raise ValueError("❌ HF_TOKEN not found in .env")

# ----------------------------
# FastAPI app
# ----------------------------
app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# ----------------------------
# InferenceClient
# ----------------------------
client = InferenceClient(token=HF_TOKEN)

# ----------------------------
# Schema
# ----------------------------

class StoryRequest(BaseModel):
    age: int
    reading_level: str
    theme: str
    gender: str  # extra feature
    description: Optional[str] = None
# ----------------------------
# Helper functions  
# function per LLM/Model call
# Each function can be traced as a child run in LangSmith
# ----------------------------
@traceable(name="Generate Story Text")
def generate_story_text(req: StoryRequest):
    print(f"start Generating story for age {req.age}, level {req.reading_level}, theme {req.theme}, Gendar {req.gender},description {req.description}")

    story_llm = ChatHuggingFace(
    llm=HuggingFaceEndpoint(
        repo_id="Qwen/Qwen2.5-7B-Instruct",
        huggingfacehub_api_token=HF_TOKEN,
        task="text-generation",
        max_new_tokens=500,
    ),
    temperature=0.65,
)
    prompt = f"""
    Create a short interactive story for a child.
    - Age: {req.age}
    - Reading level: {req.reading_level}
    - Theme: {req.theme}
    - Gender: {req.gender}
    - Format: Markdown with headings and chapters
    """
    if req.description:
        prompt = f"""
        Create a short interactive story for a child.
        - Age: {req.age}
        - Reading level: {req.reading_level}
        - Theme: {req.theme}
        - Gender: {req.gender}
        - Additional Preferences: {req.description} 
        - Format: Markdown with headings and chapters
    """
    story_response = story_llm.invoke(prompt)
    print(f"Finished generating story.", story_response)
    return story_response.content if hasattr(story_response, "content") else str(story_response)

@traceable(name="Generate Image")
def generate_image(theme: str):
    print(f"start Generating image for theme {theme}")
    image_pil = client.text_to_image(
        model="stabilityai/stable-diffusion-xl-base-1.0",
        prompt=f"cute colorful illustration for children about {theme}"
    )
    buffer = BytesIO()
    image_pil.save(buffer, format="PNG")
    image_bytes = buffer.getvalue()
    print("Finished generating image.")
    return f"data:image/png;base64,{base64.b64encode(image_bytes).decode('utf-8')}"

@traceable(name="Generate Audio")
def generate_audio(story_text: str):
    cleaned_string = re.sub(r'[^a-zA-Z0-9\s]', '', story_text)
    try:
        audio_bytes = client.text_to_speech(
            model="espnet/kan-bayashi_ljspeech_vits",
            text=cleaned_string[:300]
        )
        if audio_bytes:
            return f"data:audio/wav;base64,{base64.b64encode(audio_bytes).decode('utf-8')}"
    except Exception:
        # fallback to gTTS
        tts = gTTS(cleaned_string[:300])
        with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as f:
            tts.save(f.name)
            with open(f.name, "rb") as audio_file:
                return f"data:audio/mp3;base64,{base64.b64encode(audio_file.read()).decode('utf-8')}"

@traceable(name="Generate Video")
def generate_video(story_text: str):
    try:
        video_bytes = client.text_to_video(
            model="cerspense/zeroscope_v2_576w",
            prompt=f"A short animated scene about {story_text}, child friendly, colorful"
        )
        if video_bytes and isinstance(video_bytes, (bytes, bytearray)):
            return f"data:video/mp4;base64,{base64.b64encode(video_bytes).decode('utf-8')}"
    except Exception as e:
        print(f"⚠️ Video generation failed: {e}")
    return None


@traceable(name="Generate Storybook")  
@app.post("/generate_story/")
async def generate_story(req: StoryRequest):
    # All steps are children inside this single trace
    print(f"Received request: {req}")
    if req.age < 0 or req.age > 15:
        return {"markdown_story": "⚠️ Age must be between 0 and 15."}
    if req.reading_level not in ["Beginner", "Intermediate", "Advanced"]:
            return {"markdown_story": "⚠️ Reading level must be one of Beginner, Intermediate, Advanced."}  
    if not req.theme:
        return {"markdown_story": "⚠️ Theme must be provided."}
    story_text = generate_story_text(req)
    image_url = generate_image(story_text)
    audio_url = generate_audio(story_text)
    #video_url = generate_video(story_text) # huggingface video models are not reliable, so disabled for now
    # if we use paid api like openai, we can easily genrate video too just required to change the model and calling function

    final_story = f"""
# 📖 Adaptive Storybook: {req.theme.title()}

![Illustration]({image_url})

{story_text}

---

🔊 [Listen to narration]({audio_url})
"""
    return {"markdown_story": final_story}
