from fastapi import FastAPI
from pydantic import BaseModel
from story_generator import generate_story_outline,comic_pipeline_from_outline
from Image_generator import run_image_generator

app = FastAPI()

# =========================
# REQUEST MODELS
# =========================

class StoryRequest(BaseModel):
    prompt: str

class ComicRequest(BaseModel):
    story: str

# =========================
# ROUTES
# =========================

@app.get("/")
def read_root():
    return {"message": "API is running"}

@app.post("/generate-story")
def generate_story(request: StoryRequest):
    prompt = request.prompt

    story = generate_story_outline(prompt)
#     story = """Panel 1 - A car zooms by overhead, leaving a trail of dust and debris in its wake.
# Panel 2 - A group of three people watch in amazement.
# Panel 3 - "Did you see that?"
# Panel 4 - "I've seen stranger things."
# Panel 5 - "I wonder where it's going?"
# Panel 6 - The car disappears into the sky."""

    return {"story": story}

@app.post("/generate-comic")
def generate_comic_image(request: ComicRequest):
    print("✅ PYTHON HIT THE COMIC IMAGE ENDPOINT")

    story = request.story
    print("📖 Story received:\n", story)
    comic_final_prompt = comic_pipeline_from_outline(story)
    image_url = run_image_generator(comic_final_prompt)

    return {
        "imageUrl": image_url
    }
