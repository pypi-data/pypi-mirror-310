
import gradio as gr
from gradio_magicquill import MagicQuill
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

import base64
from PIL import Image, ImageOps
import io

css = """
.ms {
    width: 60%;
    margin: auto
}
"""
import random
import time 
def read_base64_image(base64_image):
    if base64_image.startswith("data:image/png;base64,"):
        base64_image = base64_image.split(",")[1]
    elif base64_image.startswith("data:image/jpeg;base64,"):
        base64_image = base64_image.split(",")[1]
    elif base64_image.startswith("data:image/webp;base64,"):
        base64_image = base64_image.split(",")[1]
    else:
        raise ValueError("Unsupported image format.")
    image_data = base64.b64decode(base64_image)
    image = Image.open(io.BytesIO(image_data))
    image = ImageOps.exif_transpose(image)
    return image

def generate_image(x, base_model_version, negative_prompt, dtype, stroke_as_edge, grow_size, edge_strength, color_strength, palette_resolution, inpaint_strength, seed, steps, cfg, sampler_name, scheduler):
    print(x['from_backend']['prompt'])
    time.sleep(0.5)
    
    color_img = read_base64_image(x['from_frontend']['add_color_image'])

    color_img.save("color_img.png")
    return x

with gr.Blocks(title="MagicQuill",css=css) as demo:
    with gr.Row():
        ms = MagicQuill()

    with gr.Row():
        with gr.Column():
            btn = gr.Button("Run", variant="primary")
        with gr.Column():
            with gr.Accordion("parameters"):
                base_model_version = gr.Radio(
                    label="Base Model Version",
                    choices=['SD1.5'],
                    value='SD1.5',
                    interactive=True
                )
                negative_prompt = gr.Textbox(
                    label="Negative Prompt",
                    value="",
                    interactive=True
                )
                dtype = gr.Radio(
                    label="Data Type",
                    choices=['float16', 'bfloat16', 'float32', 'float64'],
                    value='float16',
                    interactive=True
                )
                stroke_as_edge = gr.Radio(
                    label="Stroke as Edge",
                    choices=['enable', 'disable'],
                    value='enable',
                    interactive=True
                )
                grow_size = gr.Slider(
                    label="Grow Size",
                    minimum=0,
                    maximum=100,
                    value=15,
                    step=1,
                    interactive=True
                )
                edge_strength = gr.Slider(
                    label="Edge Strength",
                    minimum=0.0,
                    maximum=5.0,
                    value=0.8,
                    step=0.01,
                    interactive=True
                )
                color_strength = gr.Slider(
                    label="Color Strength",
                    minimum=0.0,
                    maximum=5.0,
                    value=0.5,
                    step=0.01,
                    interactive=True
                )
                palette_resolution = gr.Slider(
                    label="Palette Resolution",
                    minimum=128,
                    maximum=2048,
                    value=2048,
                    step=16,
                    interactive=True
                )
                inpaint_strength = gr.Slider(
                    label="Inpaint Strength",
                    minimum=0.0,
                    maximum=5.0,
                    value=1.0,
                    step=0.01,
                    interactive=True
                )
                seed = gr.Number(
                    label="Seed",
                    value=0,
                    precision=0,
                    interactive=True
                )
                steps = gr.Slider(
                    label="Steps",
                    minimum=1,
                    maximum=50,
                    value=20,
                    interactive=True
                )
                cfg = gr.Slider(
                    label="CFG",
                    minimum=0.0,
                    maximum=100.0,
                    value=4.0,
                    step=0.1,
                    interactive=True
                )
                sampler_name = gr.Dropdown(
                    label="Sampler Name",
                    choices=["euler", "euler_ancestral", "heun", "heunpp2","dpm_2", "dpm_2_ancestral", "lms", "dpm_fast", "dpm_adaptive", "dpmpp_2s_ancestral", "dpmpp_sde", "dpmpp_sde_gpu", "dpmpp_2m", "dpmpp_2m_sde", "dpmpp_2m_sde_gpu", "dpmpp_3m_sde", "dpmpp_3m_sde_gpu", "ddpm", "lcm", "ddim", "uni_pc", "uni_pc_bh2"],
                    value='euler_ancestral',
                    interactive=True
                )
                scheduler = gr.Dropdown(
                    label="Scheduler",
                    choices=["normal", "karras", "exponential", "sgm_uniform", "simple", "ddim_uniform"],
                    value='exponential',
                    interactive=True
                )

        btn.click(generate_image, inputs=[ms, base_model_version, negative_prompt, dtype, stroke_as_edge, grow_size, edge_strength, color_strength, palette_resolution, inpaint_strength, seed, steps, cfg, sampler_name, scheduler], outputs=ms)
            
app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def get_root_url(
    request: Request, route_path: str, root_path: str | None
):
    print(root_path)
    return root_path
import gradio.route_utils 
gr.route_utils.get_root_url = get_root_url

gr.mount_gradio_app(app, demo, path="/demo", root_path="/demo")

@app.post("/magic_quill/guess_prompt")
async def guess_prompt(request: Request):
    data = await request.json()
    return "mock prompt"

if __name__ == "__main__":
    # uvicorn.run(app, port=8000)
    demo.launch()