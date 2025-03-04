# app.py
import streamlit as st
from PIL import Image
import torch
from transformers import pipeline, AutoTokenizer, AutoModelForCausalLM
from diffusers import StableDiffusionPipeline, DiffusionPipeline
from sentence_transformers import SentenceTransformer
import numpy as np
import os
import faiss
import pickle
import uuid
from huggingface_hub import InferenceClient

@st.cache_resource
def get_hf_client():
    return InferenceClient(
        provider="hf-inference",
        api_key="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"  # Replace with your actual API key
    )

st.set_page_config(
    page_title="Text to Image Generator",
    page_icon="🖼️",
    layout="wide"
)
st.title("Text to Image Generator")
st.markdown("Generate images from text descriptions using LLMs and diffusion models")
user_text = st.text_area("Enter your image description:", height=150)

model_options = {
    "Stable Diffusion v1.5": "stable-diffusion-v1-5/stable-diffusion-v1-5",
    "Stable Diffusion XL": "stabilityai/stable-diffusion-xl-base-1.0",
    "Midjourney Style": "prompthero/openjourney"
}

selected_model=st.selectbox("select model",list(model_options.keys()))
generate_button = st.button("Generate Image")
if generate_button:
    if not user_text:
        st.warning("Please enter a text description first.")
    else:
        try:
            with st.spinner(f"Generating image from: '{user_text}'"):
                client = get_hf_client()
                image = client.text_to_image(
                    user_text,
                    model=model_options[selected_model]
                )
                img_filename = f"generated_images/{uuid.uuid4()}.png"
                os.makedirs("generated_images", exist_ok=True)
                image.save(img_filename)
                st.image(image, caption=f"Generated from: {user_text}")
                with open(img_filename, "rb") as file:
                    btn = st.download_button(
                        label="Download Image",
                        data=file,
                        file_name=os.path.basename(img_filename),
                        mime="image/png"
                    )
        except Exception as e:
            st.error(f"Error generating image: {str(e)}")

