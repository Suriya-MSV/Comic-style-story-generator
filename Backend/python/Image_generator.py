import json
import uuid
import requests
import time
import base64
import os

IMGBB_API_KEY = os.getenv("IMGBB_API_KEY")

POSITIVE_PROMPT = """You are generating a single comic page.

LAYOUT REQUIREMENTS:
- Create a 2×3 grid (2 columns × 3 rows)
- Exactly 6 panels total
- Panels must be read left-to-right, top-to-bottom
- Panel order:
  Row 1: Panel 1 | Panel 2
  Row 2: Panel 3 | Panel 4
  Row 3: Panel 5 | Panel 6

GLOBAL RULES:
- Use the STORY VISUAL STYLE consistently across all panels
- Maintain character consistency for Elara in every panel
- Each panel must match its corresponding PANEL IMAGE PROMPT exactly
- Render dialogue ONLY as speech bubbles inside each panel
- Do NOT add narration boxes or extra text
- Do NOT merge panels or change panel order
- One unified comic page, not separate images

TASK:
Using the information below, generate a complete 2×3 comic page image.

"""
COMFYUI_API_URL = "http://localhost:8188"
STEPS = 15

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
      "width": 2048,
      "height": 3072,
      "batch_size": 1
    },
    "class_type": "EmptySD3LatentImage",
    "_meta": {
      "title": "EmptySD3LatentImage"
    }
  },
  "31": {
    "inputs": {
      "seed": 953920934923132,
      "steps": STEPS,
      "cfg": 1,
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
      "unet_name": "flux1-krea-dev_fp8_scaled.safetensors",
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
        "107",
        0
      ]
    },
    "class_type": "DyPE_FLUX",
    "_meta": {
      "title": "DyPE"
    }
  },
  "107": {
    "inputs": {
      "lora_name": "comic strip style v2.safetensors",
      "strength_model": 1,
      "model": [
        "38",
        0
      ]
    },
    "class_type": "LoraLoaderModelOnly",
    "_meta": {
      "title": "LoraLoaderModelOnly"
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

def download_image(status_data):
    outputs = status_data.get("outputs", {})

    for node_id, node_output in outputs.items():
        if "images" not in node_output:
            continue

        for image in node_output["images"]:
            params = {
                "filename": image["filename"],
                "type": image.get("type", "output")
            }

            if image.get("subfolder"):
                params["subfolder"] = image["subfolder"]

            response = requests.get(f"{COMFYUI_API_URL}/view", params=params)

            if response.status_code == 200:
                print("Uploading image to ImgBB...")
                image_url = upload_to_imgbb(response.content)
                print("✅ Image URL:", image_url)
                return image_url

    raise Exception("No image generated")

def upload_to_imgbb(image_bytes):
    """
    Uploads image bytes to ImgBB and returns the public URL.
    """
    if not IMGBB_API_KEY:
        raise Exception("ImgBB API key not found in environment")

    encoded = base64.b64encode(image_bytes).decode("utf-8")

    response = requests.post(
        "https://api.imgbb.com/1/upload",
        data={
            "key": IMGBB_API_KEY,
            "image": encoded
        }
    )

    if response.status_code != 200:
        raise Exception(f"ImgBB upload failed: {response.text}")

    return response.json()["data"]["url"]

def main():
    prompt_id = submit_workflow()
    status_data = wait_for_completion(prompt_id)
    image_url = download_image(status_data)
    return image_url


def run_image_generator(prompt):
    global POSITIVE_PROMPT
    POSITIVE_PROMPT = POSITIVE_PROMPT + "\n\n" + prompt
    return main()
