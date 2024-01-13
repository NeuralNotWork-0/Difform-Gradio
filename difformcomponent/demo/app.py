
import gradio as gr
from gradio_difformcomponent import DifformComponent
from gradio_difformcomponent.difform.dkg import DifformKnowledgeGraph

difform_path = "../demo_data"

def log_audio(x):
    sample_rate, audio = x
    return {
        'type': 'audio',
        'args': {
            'mode': 'test',
            'model_name': 'demo',
            'seed': 0,
            'sample_rate': sample_rate,
            'output': audio
        },
        'value': x
    }

with gr.Blocks() as demo:
    with gr.Row():
        with gr.Column():
            audio_in = gr.Audio()
            log_btn = gr.Button(value="Log")
        with gr.Column():
            difform = DifformComponent(difform_path)
            audio_out = gr.Audio(interactive=False)
    log_btn.click(log_audio, inputs=audio_in, outputs=difform)

demo.launch()
