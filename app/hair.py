import torch
from PIL import Image
from diffusers import StableDiffusionPipeline
import io
import os
import uuid

# Load the fine-tuned model once
pipe = StableDiffusionPipeline.from_pretrained(
    "models/hair_model",
    torch_dtype=torch.float16
).to("cuda")

def run_hair_inference(image_bytes, hair_style, color):
    # Load and convert image to RGB
    image = Image.open(image_bytes).convert("RGB")

    # Create prompt
    prompt = f"portrait of a person with {color + ' ' if color else ''}{hair_style} hairstyle"

    # Run inference
    output = pipe(prompt=prompt, image=image, num_inference_steps=25).images[0]

    # Save result
    filename = f"{uuid.uuid4().hex}.png"
    result_path = os.path.join("app/static/results", filename)
    os.makedirs(os.path.dirname(result_path), exist_ok=True)
    output.save(result_path)

    return f"/static/results/{filename}"
