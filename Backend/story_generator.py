import os
import re
import textwrap
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()
API_KEY = os.getenv("GOOGLE_API_KEY")
if not API_KEY:
    raise SystemExit("Set GOOGLE_API_KEY in environment or .env")

genai.configure(api_key=API_KEY)
MODEL = genai.GenerativeModel(
    model_name="models/gemini-2.5-flash",
    generation_config={
        "temperature": 0.8,
        "top_p": 0.9,
        "top_k": 40,
        "max_output_tokens": 2048
    }
)


# -----------------------
# Helpers
# -----------------------
def user_yes(prompt="Approve this? (yes / no): "):
    r = input(prompt).strip().lower()
    return r in ("y", "yes")


def approval_step(output_text, stage_name):
    print("\n" + "=" * 60)
    print(f"📝 {stage_name} OUTPUT")
    print("=" * 60)
    print(output_text)
    print("\nDo you approve this? (yes / no)")
    if user_yes("> "):
        return output_text
    print("\nEnter the changes you want (single line):")
    changes = input("> ").strip()
    # Ask model to apply changes
    prompt = (
        f"Here is the previous {stage_name.lower()}:\n\n{output_text}\n\n"
        f"Apply these requested changes in a coherent way: {changes}\n\n"
        "Return only the revised output (do not include commentary)."
    )
    response = MODEL.generate_content(prompt, temperature=0.7)
    return response.text


def call_model_system(prompt):
    resp = MODEL.generate_content(prompt)
    return resp.text


# -----------------------
# STEP 1: Generate concise story
# -----------------------
def generate_short_story(description, max_words=250):
    prompt = textwrap.dedent(
        f"""
        Write a short, self-contained fictional story from this description.
        Keep the whole story under {max_words} words (concise and focused).
        Include clear character names, a beginning, a conflict and a small resolution.
        Keep language simple and cinematic; do NOT produce scene breakdowns here, just the story body.
        
        DESCRIPTION:
        {description}
        """
    )
    return call_model_system(prompt)


# -----------------------
# STEP 2: Produce exactly N scenes
# -----------------------
def request_scenes_from_model(story_text, target_scenes=6):
    prompt = textwrap.dedent(
        f"""
        Split the following story into exactly {target_scenes} numbered SCENES.
        Output format MUST be a numbered list like:
        1. Scene Title
           Description: <one-paragraph description of setting & action>
           Characters: <comma-separated characters present>

        Provide exactly {target_scenes} scenes. Make sure the scenes collectively cover the whole story.
        
        STORY:
        {story_text}
        """
    )
    return call_model_system(prompt)


def parse_numbered_scenes(scenes_text):
    # split at lines that start with a number + dot
    blocks = re.split(r'\n(?=\s*\d+\.)', scenes_text.strip())
    scenes = []
    for block in blocks:
        # block begins with "1. Title"
        m_title = re.match(r'\s*(\d+)\.\s*(.+)', block)
        if not m_title:
            continue
        # split lines to find Description and Characters
        title_line, *rest = block.splitlines()
        title = m_title.group(2).strip()
        desc_match = re.search(r'Description:\s*(.+)', block, re.DOTALL | re.IGNORECASE)
        chars_match = re.search(r'Characters:\s*(.+)', block, re.IGNORECASE)
        description = desc_match.group(1).strip() if desc_match else ""
        characters = chars_match.group(1).strip() if chars_match else ""
        scenes.append({"title": title, "description": description, "characters": characters})
    return scenes


def ensure_exact_scenes(story, target=6, tries=3):
    # Try re-prompting the model up to `tries` times to get exactly `target` scenes.
    for attempt in range(tries):
        raw = request_scenes_from_model(story, target_scenes=target)
        sc = parse_numbered_scenes(raw)
        if len(sc) == target:
            return sc, raw
        # otherwise re-prompt with explicit instruction referencing previous attempt
        story = story  # unchanged, but we'll include previous raw in next prompt
        followup_prompt = textwrap.dedent(
            f"""
            Previous attempt to create exactly {target} scenes produced {len(sc)} scenes.
            Previous output was:
            {raw}

            Please re-split the original story into exactly {target} scenes.
            Ensure numbering 1..{target}, and include Title, Description, and Characters for each.
            STORY:
            {story}
            """
        )
        raw = call_model_system(followup_prompt)
        sc = parse_numbered_scenes(raw)
        if len(sc) == target:
            return sc, raw
    # fallback: programmatically split the story into `target` chunks by sentences
    fallback = programmatic_scene_split(story, target)
    fallback_text = programmatic_scenes_to_text(fallback)
    return fallback, fallback_text


def programmatic_scene_split(story, target):
    # naive fallback: split story into sentences and chunk into target groups
    sentences = re.split(r'(?<=[.!?])\s+', story.strip())
    chunks = [[] for _ in range(target)]
    # distribute sentences round-robin then join to form scene descriptions
    for i, s in enumerate(sentences):
        chunks[i % target].append(s)
    scenes = []
    for i, chunk in enumerate(chunks, 1):
        desc = " ".join(chunk).strip()
        title = f"Scene {i}"
        scenes.append({"title": title, "description": desc, "characters": ""})
    return scenes


def programmatic_scenes_to_text(scenes):
    parts = []
    for i, s in enumerate(scenes, 1):
        parts.append(f"{i}. {s['title']}\n   Description: {s['description']}\n   Characters: {s['characters']}")
    return "\n\n".join(parts)


# -----------------------
# STEP 3: Generate dialogue for each scene
# -----------------------
def generate_dialogue_for_scene(scene, story_context):
    prompt = textwrap.dedent(
        f"""
        You are writing screenplay-style dialogue for a comic. Using the scene below,
        write natural-sounding short dialogues between the characters listed.
        Keep it compact—each scene's dialogue should be at most ~10-20 lines total.
        Maintain tone consistent with the story.

        Scene Title: {scene['title']}
        Scene Description: {scene['description']}
        Characters: {scene['characters']}

        STORY (for reference): {story_context}

        Output only the dialogue lines, prefixing each line with the speaker followed by ":".
        """
    )
    return call_model_system(prompt)


# -----------------------
# STEP 4: Create compact image prompts for comic panels
# -----------------------
def generate_image_prompt_for_scene(scene, story_context, style_hint="dynamic comic, cinematic panels, high contrast"):
    prompt = textwrap.dedent(
        f"""
        Create a concise image-generation prompt (one or two sentences) for a comic panel
        that visually captures this scene for an illustrator or an image generator.
        Include: main characters and their poses, key foreground/background elements,
        emotional tone, time of day, and an art-style hint.

        Scene Title: {scene['title']}
        Scene Description: {scene['description']}
        Characters: {scene['characters']}

        Story context: {story_context}

        Output as a single short sentence suitable to pass to an image generator.
        Add the style hint: {style_hint}
        """
    )
    return call_model_system(prompt)


# -----------------------
# MAIN PIPELINE
# -----------------------
def pipeline():
    print("Enter your story description: ")
    description = input("> ").strip()

    # 1) Short story
    story = generate_short_story(description, max_words=220)
    story = approval_step(story, "STORY GENERATION")

    # 2) Scenes (exactly 6)
    scenes_list, scenes_raw = ensure_exact_scenes(story, target=6)
    # show the raw formatted scenes for approval
    scenes_raw = approval_step(scenes_raw, "SCENE BREAKDOWN")
    # if user edited scenes_raw (revised by model), re-parse to scenes_list
    scenes_list = parse_numbered_scenes(scenes_raw)
    if len(scenes_list) != 6:
        # parse fallback
        scenes_list = ensure_exact_scenes(story, target=6)[0]

    # 3) Dialogues per scene
    dialogues_by_scene = []
    for idx, scene in enumerate(scenes_list, 1):
        print(f"\nGenerating dialogue for scene {idx}: {scene['title']}")
        dialogue = generate_dialogue_for_scene(scene, story)
        dialogue = approval_step(dialogue, f"DIALOGUE (Scene {idx})")
        dialogues_by_scene.append(dialogue)

    # 4) Image prompts per scene
    image_prompts = []
    for idx, scene in enumerate(scenes_list, 1):
        img_prompt = generate_image_prompt_for_scene(scene, story)
        # let user tweak image prompt
        img_prompt = approval_step(img_prompt, f"IMAGE PROMPT (Scene {idx})")
        image_prompts.append(img_prompt)

    # FINAL OUTPUT
    print("\n" + "=" * 80)
    print("🎉 FINAL COMIC STORY PACKAGE")
    print("=" * 80)
    print("\n--- SHORT STORY ---\n")
    print(story)
    print("\n--- SCENES (6) ---\n")
    for i, s in enumerate(scenes_list, 1):
        print(f"{i}. {s['title']}")
        print(f"   Description: {s['description']}")
        print(f"   Characters: {s['characters']}\n")
    print("\n--- DIALOGUES ---\n")
    for i, d in enumerate(dialogues_by_scene, 1):
        print(f"Scene {i} Dialogue:\n{d}\n")
    print("\n--- IMAGE PROMPTS (for comic panels) ---\n")
    for i, ip in enumerate(image_prompts, 1):
        print(f"Scene {i} image prompt: {ip}\n")

    # Pack as a dict to use programmatically if you want to send to backend
    final_package = {
        "story": story,
        "scenes": scenes_list,
        "dialogues": dialogues_by_scene,
        "image_prompts": image_prompts,
    }
    return final_package


if __name__ == "__main__":
    pipeline()
