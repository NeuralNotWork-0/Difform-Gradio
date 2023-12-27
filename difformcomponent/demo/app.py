
import gradio as gr
from gradio_difformcomponent import DifformComponent


example = DifformComponent().example_inputs()

demo = gr.Interface(
    lambda x:x,
    DifformComponent(),  # interactive version of your component
    DifformComponent(),  # static version of your component
    # examples=[[example]],  # uncomment this line to view the "example version" of your component
)


demo.launch()
