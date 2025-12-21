import os
import time
import textwrap
from dotenv import load_dotenv
from sambanova import SambaNova
from requests.exceptions import RequestException
import google.generativeai as genai

# =======================
# ENV SETUP
# =======================
load_dotenv()

SAMBANOVA_API_KEY = os.getenv("SAMBANOVA_API_KEY")
GEMINI_API_KEY = os.getenv("GOOGLE_API_KEY")

if not SAMBANOVA_API_KEY:
    raise SystemExit("❌ Set SAMBANOVA_API_KEY in environment or .env")

if not GEMINI_API_KEY:
    raise SystemExit("❌ Set GEMINI_API_KEY in environment or .env")

# =======================
# SAMBANOVA CLIENT
# =======================
sambanova_client = SambaNova(
    api_key=SAMBANOVA_API_KEY,
    base_url="https://api.sambanova.ai/v1",
)

SAMBANOVA_MODEL = "ALLaM-7B-Instruct-preview"

# =======================
# GEMINI CLIENT
# =======================
genai.configure(api_key=GEMINI_API_KEY)
GEMINI_MODEL =  genai.GenerativeModel(
    model_name="models/gemini-2.5-flash",
    generation_config={
        "temperature": 0.8,
        "top_p": 0.9,
        "top_k": 40
    }
)

# =======================
# SAFE CALL WITH RETRY
# =======================
def call_sambanova(prompt, max_retries=1, delay=8):
    for attempt in range(1, max_retries + 1):
        try:
            response = sambanova_client.chat.completions.create(
                model=SAMBANOVA_MODEL,
                messages=[
                    {
                        "role": "system",
                        "content": "You are a professional comic book writer and visual storyteller."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                temperature=0.8,
                top_p=0.9,
            )

            content = response.choices[0].message.content
            if not content:
                raise ValueError("Empty response from SambaNova")

            return content.strip()

        except (RequestException, ValueError) as e:
            print(f"⚠️ SambaNova Error: {e}")
            if attempt < max_retries:
                print(f"🔁 Retrying in {delay}s...")
                time.sleep(delay)
            else:
                raise

    raise SystemExit("❌ SambaNova max retries exceeded")

# =======================
# GEMINI IMAGE PROMPT HIT
# =======================
def generate_image_prompts_with_gemini(panels):
    print("\n--- FINAL HIT: Gemini Image Prompt Generation ---")

    panels_text = "\n\n".join(
        [f"PANEL {i+1}:\n{panel}" for i, panel in enumerate(panels)]
    )

    gemini_prompt = f"""
You are a professional comic-book visual designer.

TASK:
1. First, describe the overall visual style of the entire comic story.
2. Then, generate image prompts for ALL comic panels in ONE response.

SECTION 1 — STORY VISUAL STYLE (MANDATORY):
Explain the overall design style of the comic in 3–4 lines:
- Climate (weather, time of day)
- Color palette
- Texture & art style
- Mood & atmosphere

SECTION 2 — COMIC PANEL IMAGE PROMPTS

STRICT GLOBAL RULES:
- Exactly 6 panels
- Each panel MUST be under 40 words
- Describe environment, characters, and mood briefly
- Include dialogue as SPEECH BUBBLE text
- No explanations
- No extra text before or after
- Follow the format EXACTLY

FORMAT EXACTLY:

STORY VISUAL STYLE:
<3–4 concise lines describing climate, colors, texture, mood>

PANEL 1 IMAGE PROMPT:
<image description under 40 words>
SPEECH BUBBLE:
<Character>: "<dialogue>"

PANEL 2 IMAGE PROMPT:
<image description under 40 words>
SPEECH BUBBLE:
<Character>: "<dialogue>"

PANEL 3 IMAGE PROMPT:
<image description under 40 words>
SPEECH BUBBLE:
<Character>: "<dialogue>"

PANEL 4 IMAGE PROMPT:
<image description under 40 words>
SPEECH BUBBLE:
<Character>: "<dialogue>"

PANEL 5 IMAGE PROMPT:
<image description under 40 words>
SPEECH BUBBLE:
<Character>: "<dialogue>"

PANEL 6 IMAGE PROMPT:
<image description under 40 words>
SPEECH BUBBLE:
<Character>: "<dialogue>"

COMIC PANELS CONTENT:
{{INSERT ALL 6 PANEL DESCRIPTIONS HERE}}
"""

    response = GEMINI_MODEL.generate_content(gemini_prompt)
    return response.text.strip()

# =======================
# MAIN COMIC PIPELINE
# =======================
# def run_comic_pipeline(user_description):

#     # -----------------------
#     # HIT 1: STORY OUTLINE
#     # -----------------------
#     print("\n--- HIT 1: Generating Story Outline ---")

#     outline_prompt = f"""
# Create a 6-panel comic story outline for the following idea:

# "{user_description}"

# RULES:
# - Exactly 6 panels
# - One sentence per panel
# - Clear beginning → climax → ending

# FORMAT:
# 1. Panel 1 - ...
# 2. Panel 2 - ...
# 3. Panel 3 - ...
# 4. Panel 4 - ...
# 5. Panel 5 - ...
# 6. Panel 6 - ...
# """

#     outline = call_sambanova(outline_prompt)
#     print("\n📘 STORY OUTLINE:\n")
#     print(outline)

#     # -----------------------
#     # HIT 2: PANEL GENERATION
#     # -----------------------
#     print("\n--- HIT 2: Generating Comic Panels ---")

#     panels = []

#     for i in range(1, 7):
#         print(f"🖊️ Generating Panel {i}...")

#         panel_prompt = textwrap.dedent(f"""
# Expand Panel {i} into a detailed comic panel.

# STORY OUTLINE:
# {outline}

# PANEL {i} MUST INCLUDE:
# - Scene title
# - Visual description (actions + setting)
# - Character descriptions
# - Lighting & mood
# - Dialogue (Character: "Dialogue")

# IMPORTANT:
# Output ONLY Panel {i}.
# """)

#         panel_text = call_sambanova(panel_prompt)
#         panels.append(panel_text)

#     # -----------------------
#     # FINAL HIT: GEMINI
#     # -----------------------
#     image_prompts = generate_image_prompts_with_gemini(panels)

#     # -----------------------
#     # FINAL OUTPUT
#     # -----------------------
#     print("\n" + "=" * 80)
#     print("🎨 FINAL IMAGE GENERATION PROMPTS (GEMINI)")
#     print("=" * 80)
#     print(image_prompts)


# =======================
# ENTRY POINT
# =======================
def generate_story_outline(user_description):
    """
    Generates a 6-panel comic story outline from user description.
    Returns the outline text.
    """
    print("\n--- Generating Story Outline ---")

    outline_prompt = f"""
Create a 6-panel comic story outline for the following idea:

"{user_description}"

RULES:
- Exactly 6 panels
- One sentence per panel
- Clear beginning → climax → ending

FORMAT:
1. Panel 1 - ...
2. Panel 2 - ...
3. Panel 3 - ...
4. Panel 4 - ...
5. Panel 5 - ...
6. Panel 6 - ...
"""

    outline = call_sambanova(outline_prompt)
    print("\n📘 STORY OUTLINE:\n")
    print(outline)

    return outline

def comic_pipeline_from_outline(story_outline):
    """
    Given a story outline, generate:
    1. 6 detailed comic panels
    2. Gemini image prompts for all panels
    Returns a dict with panels and image prompts.
    """
    print("\n--- Generating Comic Panels ---")

    panels = []
    for i in range(1, 7):
        print(f"🖊️ Generating Panel {i}...")
        panel_prompt = textwrap.dedent(f"""
Expand Panel {i} into a detailed comic panel.

STORY OUTLINE:
{story_outline}

PANEL {i} MUST INCLUDE:
- Scene title
- Visual description (actions + setting)
- Character descriptions
- Lighting & mood
- Dialogue (Character: "Dialogue")

IMPORTANT:
Output ONLY Panel {i}.
""")
        panel_text = call_sambanova(panel_prompt)
        panels.append(panel_text)

    print("\n--- Generating Gemini Image Prompts ---")
    image_prompts = generate_image_prompts_with_gemini(panels)

    print("\n" + "=" * 80)
    print("🎨 FINAL IMAGE GENERATION PROMPTS (GEMINI)")
    print("=" * 80)
    print(image_prompts)

    return {
        "panels": panels,
        "image_prompts": image_prompts
    }