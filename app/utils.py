# import necessary libraries
import os
from flask import session, jsonify
from PIL import Image
from io import BytesIO
from time import sleep
from transformers import pipeline, set_seed, AutoTokenizer, AutoModelForCausalLM
from flask_login import login_required
import torch

# Load LLaMA 3
model_name = "meta-llama/Llama-3-7b-hf"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForCausalLM.from_pretrained(model_name, device_map="auto", torch_dtype=torch.float16)

@login_required
def chat_with_ai(user_input, image_path, chat_history):
    """
    Function to interact with the AI model and return a response.
    """
    # Load the image if provided
    image = None
    if image_path:
        image = Image.open(image_path)
        image = image.convert("RGB")
        image_bytes = BytesIO()
        image.save(image_bytes, format='PNG')
        # NOTE: Currently, the image is not passed to the model (LLaMA 3 is text-only).
        # You can later add CLIP or BLIP for visual reasoning if needed.

    # Build chat history text for prompt
    prompt = ""
    for msg in chat_history:
        role = msg["role"]
        content = msg["content"]
        if role == "user":
            prompt += f"User: {content}\n"
        elif role == "assistant":
            prompt += f"Assistant: {content}\n"
    prompt += f"User: {user_input}\nAssistant:"

    # Tokenize the prompt
    inputs = tokenizer(prompt, return_tensors="pt").to(model.device)

    # Generate response
    with torch.no_grad():
        output = model.generate(
            **inputs,
            max_new_tokens=200,
            temperature=0.7,
            top_p=0.95,
            do_sample=True,
            pad_token_id=tokenizer.eos_token_id,
        )

    # Decode only the newly generated text
    decoded_output = tokenizer.decode(output[0][inputs['input_ids'].shape[-1]:], skip_special_tokens=True)

    return decoded_output.strip()
