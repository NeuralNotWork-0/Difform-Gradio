    
import gradio as gr
from gradio_difformcomponent import DifformComponent


demo = gr.Interface(
    lambda x:x,
    DifformComponent(),  # interactive version of your component
    gr.Audio(),  # static version of your component
    # examples=[[example]],  # uncomment this line to view the "example version" of your component
)


demo.launch()
