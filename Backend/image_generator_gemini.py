import os
import requests
import base64
import json
from dotenv import load_dotenv

# Load API key
load_dotenv()
API_KEY = os.getenv("GOOGLE_API_KEY")
if not API_KEY:
    raise ValueError("Missing GOOGLE_API_KEY in .env file!")

# Endpoint for Gemini image generation
url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash-image:generateContent?key={API_KEY}"

# Prompt in the required REST JSON format
payload = {
    "contents": [
        {
            "role": "user",
            "parts": [
                {
                    "text": "A boy finds a magical camera on the street, cinematic comic style"
                }
            ]
        }
    ]
}

# Send request
response = requests.post(url, json=payload)
data = response.json()

# Debug: Uncomment to inspect the full JSON response
# print(json.dumps(data, indent=2))

# Error handling
if "error" in data:
    print("Error in API response:")
    print(json.dumps(data["error"], indent=2))
    exit(1)

# Process output parts including image(s)
output_parts = data.get("candidates", [])[0].get("content", {}).get("parts", [])

# Loop through parts and save images
image_count = 0
for part in output_parts:
    inline = part.get("inlineData")
    if inline and "data" in inline:
        image_bytes = base64.b64decode(inline["data"])
        filename = f"output_{image_count}.png"
        with open(filename, "wb") as f:
            f.write(image_bytes)
        print(f"Saved image: {filename}")
        image_count += 1

if image_count == 0:
    print("No images found in response.")
