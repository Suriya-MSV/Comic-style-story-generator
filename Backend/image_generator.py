import json
import uuid
import requests
import time

POSITIVE_PROMPT = """A small comic story shown in four panels arranged in a 2x2 grid.

Panel 1:
A young Indian college student finds an old dusty camera inside a wooden box in a quiet room.
The camera looks mysterious and slightly glowing.
Clear white speech bubble saying:
"Where did this come from?"

Panel 2:
The student points the camera at a messy room and presses the shutter.
A bright magical flash fills the panel.
Clear white speech bubble saying:
"Let me try it."

Panel 3:
The room is now clean and beautiful, filled with warm light.
The student looks shocked and amazed, holding the camera.
Clear white speech bubble saying:
"It changed everything!"

Panel 4:
The student smiles and carefully puts the camera back into the box.
The camera softly glows.
Clear white speech bubble saying:
"Some magic is better used gently."

Art style:
Clean digital comic illustration.
Bold black outlines.
Smooth soft shading.
Warm, vibrant colors.
Consistent character design across all panels.
Not photorealistic, clearly illustrated.

Layout:
Clear panel borders.
Speech bubbles fully inside panels.
Large, easy-to-read text.

Camera:
Medium shots, straight-on view.

Lighting:
Soft indoor lighting with magical glow effects.

Mood:
Wholesome, magical, calm.
High detail, sharp focus.
"""
NEGATIVE_PROMPT = ""
COMFYUI_API_URL = "http://localhost:8188"
HEIGHT = 1024
WIDTH = 1024
SEED = 1078347424916127
STEPS = 25
CFG = 1
CHECHPOINT_NAME = "flux1-krea-dev_fp8_scaled.safetensors"

def create_workflow():
    workflow = {
  "8": {
    "inputs": {
      "samples": [
        "31",
        0
      ],
      "vae": [
        "39",
        0
      ]
    },
    "class_type": "VAEDecode",
    "_meta": {
      "title": "VAE Decode"
    }
  },
  "27": {
    "inputs": {
      "width": WIDTH,
      "height": HEIGHT,
      "batch_size": 1
    },
    "class_type": "EmptySD3LatentImage",
    "_meta": {
      "title": "EmptySD3LatentImage"
    }
  },
  "31": {
    "inputs": {
      "seed": SEED,
      "steps": STEPS,
      "cfg": CFG,
      "sampler_name": "euler",
      "scheduler": "beta",
      "denoise": 1,
      "model": [
        "106",
        0
      ],
      "positive": [
        "45",
        0
      ],
      "negative": [
        "42",
        0
      ],
      "latent_image": [
        "27",
        0
      ]
    },
    "class_type": "KSampler",
    "_meta": {
      "title": "KSampler"
    }
  },
  "38": {
    "inputs": {
      "unet_name": CHECHPOINT_NAME,
      "weight_dtype": "default"
    },
    "class_type": "UNETLoader",
    "_meta": {
      "title": "Load Diffusion Model"
    }
  },
  "39": {
    "inputs": {
      "vae_name": "ae.safetensors"
    },
    "class_type": "VAELoader",
    "_meta": {
      "title": "Load VAE"
    }
  },
  "40": {
    "inputs": {
      "clip_name1": "clip_l.safetensors",
      "clip_name2": "t5xxl_fp8_e4m3fn_scaled.safetensors",
      "type": "flux",
      "device": "default"
    },
    "class_type": "DualCLIPLoader",
    "_meta": {
      "title": "DualCLIPLoader"
    }
  },
  "42": {
    "inputs": {
      "conditioning": [
        "45",
        0
      ]
    },
    "class_type": "ConditioningZeroOut",
    "_meta": {
      "title": "ConditioningZeroOut"
    }
  },
  "45": {
    "inputs": {
      "text": POSITIVE_PROMPT,
      "clip": [
        "40",
        0
      ]
    },
    "class_type": "CLIPTextEncode",
    "_meta": {
      "title": "CLIP Text Encode (Prompt)"
    }
  },
  "55": {
    "inputs": {
      "tile_size": 512,
      "overlap": 64,
      "temporal_size": 64,
      "temporal_overlap": 8,
      "samples": [
        "31",
        0
      ],
      "vae": [
        "39",
        0
      ]
    },
    "class_type": "VAEDecodeTiled",
    "_meta": {
      "title": "VAE Decode (Tiled)"
    }
  },
  "104": {
    "inputs": {
      "filename_prefix": "flux_dype",
      "images": [
        "55",
        0
      ]
    },
    "class_type": "SaveImage",
    "_meta": {
      "title": "Save Image"
    }
  },
  "106": {
    "inputs": {
      "width": 2048,
      "height": 2048,
      "model_type": "auto",
      "method": "vision_yarn",
      "yarn_alt_scaling": False,
      "enable_dype": True,
      "base_resolution": 1024,
      "dype_start_sigma": 1,
      "dype_scale": 2,
      "dype_exponent": 2,
      "base_shift": 0.5,
      "max_shift": 1.15,
      "model": [
        "38",
        0
      ]
    },
    "class_type": "DyPE_FLUX",
    "_meta": {
      "title": "DyPE"
    }
  }
}

    return workflow

def generate_client_id():
    return str(uuid.uuid4())

def submit_workflow():
    workflow = create_workflow()
    client_id = generate_client_id()

    payload = {
        "prompt": workflow,
        "client_id": client_id
    }

    print("Submitting workflow to ComfyUI...")
    response = requests.post(f"{COMFYUI_API_URL}/prompt", json=payload)

    if response.status_code != 200:
        raise Exception(f"Failed to submit workflow: {response.text}")

    data = response.json()
    prompt_id = data.get("prompt_id")

    print("Queued prompt:", prompt_id)
    return prompt_id

def wait_for_completion(prompt_id):
    print("Waiting for workflow to complete...")

    while True:
        response = requests.get(f"{COMFYUI_API_URL}/history/{prompt_id}")
        if response.status_code != 200:
            time.sleep(1)
            continue

        data = response.json()
        if prompt_id in data:
            print("Workflow completed.")
            return data[prompt_id]

        time.sleep(1)

def download_image(status_data, prompt_id):
    prompt_data = status_data.get(prompt_id)
    if not prompt_data:
        raise Exception("Prompt ID not found in history data.")

    outputs = prompt_data.get("outputs", {})
    image_count = 0

    for node_id, node_output in outputs.items():
        if "images" not in node_output:
            continue

        for image in node_output["images"]:
            filename = image["filename"]
            subfolder = image.get("subfolder", "")
            image_type = image.get("type", "output")

            print(f"Downloading image: {filename} (node {node_id})")

            params = {
                "filename": filename,
                "type": image_type
            }
            if subfolder:
                params["subfolder"] = subfolder

            response = requests.get(f"{COMFYUI_API_URL}/view", params=params)

            if response.status_code == 200:
                out_name = f"downloaded_{image_count}.png"
                with open(out_name, "wb") as f:
                    f.write(response.content)

                print(f"Saved: {out_name}")
                image_count += 1
            else:
                print("Failed to download:", response.text)

    if image_count == 0:
        print("⚠️ No images found in outputs (but generation succeeded).")
    else:
        print(f"✅ Downloaded {image_count} image(s)")

def main():
    print("="*50)
    print("Starting image generation workflow...")
    print("="*50)

    prompt_id = submit_workflow()
    if not prompt_id:
        print("No prompt ID returned. Exiting.")
        return
    
    status_data = wait_for_completion(prompt_id)

    if not status_data:
        print("No status data returned. Exiting.")
        return
    
    download_image(status_data, prompt_id)

if __name__ == "__main__":
    main()