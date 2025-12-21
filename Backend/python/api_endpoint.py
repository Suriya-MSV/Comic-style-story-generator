from fastapi import FastAPI
from pydantic import BaseModel
from story_generator import generate_story_outline

app = FastAPI()
@app.get("/")
def read_root():
    return {"message": "API is running"}

@app.post("/generate-story")
def generate_story(request: dict):
    prompt = request.get("prompt", "")
    # Here you would add the logic to generate a story based on the prompt
    story = generate_story_outline(prompt)
    return {story}