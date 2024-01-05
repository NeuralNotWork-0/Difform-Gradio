
import gradio as gr
from gradio_difformcomponent import DifformComponent

difform_path = "./demo/data"

with gr.Blocks() as demo:
    with gr.Row():
        with gr.Column():
            audio_in = gr.Audio()
        with gr.Column():
            difform = DifformComponent(difform_path=difform_path)
            audio_out = gr.Audio(interactive=False)

demo.launch()
