from diffusers import StableDiffusionPipeline
import torch

# Load a public comic-style Stable Diffusion model
pipe = StableDiffusionPipeline.from_pretrained(
    "runwayml/stable-diffusion-v1-5",  # comic/manga style
    torch_dtype=torch.float16
)
pipe = pipe.to("cuda")  # use GPU

# Prompt with empty speech bubble
prompt = ("a boy standing infront of a car. in comic style and add a empty speech bubble above the head no test in the bubble.")

# Generate image
image = pipe(prompt, guidance_scale=7.5).images[0]

# Save the image
image.save("parrot_comic.png")
print("Image saved as parrot_comic.png")
