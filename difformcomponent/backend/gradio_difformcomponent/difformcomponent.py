from __future__ import annotations

import dataclasses
from pathlib import Path
from typing import Any, Literal

from gradio import processing_utils
from gradio.components.base import Component
from gradio.events import Events
from gradio.data_classes import FileData

from .difform.dkg import DifformKnowledgeGraph

@dataclasses.dataclass
class WaveformOptions:
    """
    A dataclass for specifying options for the waveform display in the Audio component. An instance of this class can be passed into the `waveform_options` parameter of `gr.Audio`.
    Parameters:
        waveform_color: The color (as a hex string or valid CSS color) of the full waveform representing the amplitude of the audio. Defaults to a light gray color.
        waveform_progress_color: The color (as a hex string or valid CSS color) that the waveform fills with to as the audio plays. Defaults to an orange color.
        show_recording_waveform: Whether to show the waveform when recording audio. Defaults to True.
        show_controls: Whether to show the standard HTML audio player below the waveform when recording audio or playing recorded audio. Defaults to False.
        skip_length: The percentage (between 0 and 100) of the audio to skip when clicking on the skip forward / skip backward buttons. Defaults to 5.
    """

    waveform_color: str = "#9ca3af"
    waveform_progress_color: str = "#f97316"
    show_recording_waveform: bool = True
    show_controls: bool = False
    skip_length: int | float = 5


class DifformComponent(Component):

    EVENTS = [
        Events.change,
        Events.input,
        Events.submit,
    ]

    def __init__(
        self,
        difform_path: str,
        value: any | None = None,
        *,
        placeholder: str | None = None,
        label: str | None = "Difform",
        every: float | None = None,
        show_label: bool | None = None,
        scale: int | None = None,
        min_width: int = 160,
        interactive: bool | None = None,
        visible: bool = True,
        rtl: bool = False,
        elem_id: str | None = None,
        elem_classes: list[str] | str | None = None,
        render: bool = True,
        format: Literal["wav", "mp3"] = "wav",
        waveform_options: WaveformOptions | dict | None = None,
    ):
        """
        Parameters:
            value: default text to provide in textbox. If callable, the function will be called whenever the app loads to set the initial value of the component.
            placeholder: placeholder hint to provide behind textbox.
            label: component name in interface.
            every: If `value` is a callable, run the function 'every' number of seconds while the client connection is open. Has no effect otherwise. Queue must be enabled. The event can be accessed (e.g. to cancel it) via this component's .load_event attribute.
            show_label: if True, will display label.
            scale: relative width compared to adjacent Components in a Row. For example, if Component A has scale=2, and Component B has scale=1, A will be twice as wide as B. Should be an integer.
            min_width: minimum pixel width, will wrap if not sufficient screen space to satisfy this value. If a certain scale value results in this Component being narrower than min_width, the min_width parameter will be respected first.
            interactive: if True, will be rendered as an editable textbox; if False, editing will be disabled. If not provided, this is inferred based on whether the component is used as an input or output.
            visible: If False, component will be hidden.
            rtl: If True and `type` is "text", sets the direction of the text to right-to-left (cursor appears on the left of the text). Default is False, which renders cursor on the right.
            elem_id: An optional string that is assigned as the id of this component in the HTML DOM. Can be used for targeting CSS styles.
            elem_classes: An optional list of strings that are assigned as the classes of this component in the HTML DOM. Can be used for targeting CSS styles.
            render: If False, component will not render be rendered in the Blocks context. Should be used if the intention is to assign event listeners now but render the component later.
        """
        self.dkg = DifformKnowledgeGraph(difform_path)
        self.placeholder = placeholder
        self.rtl = rtl
        self.format = format
        if waveform_options is None:
            self.waveform_options = WaveformOptions()
        self.waveform_options = (
            WaveformOptions(**waveform_options)
            if isinstance(waveform_options, dict)
            else waveform_options
        )
        super().__init__(
            label=label,
            every=every,
            show_label=show_label,
            scale=scale,
            min_width=min_width,
            interactive=interactive,
            visible=visible,
            elem_id=elem_id,
            elem_classes=elem_classes,
            value=value,
            render=render,
        )

    def preprocess(self, x: dict | None) -> str | None:
        return None if x is None else str(x)

    def postprocess(self, y: dict | None) -> dict | None:
        out = {}
        if y is not None:
            y_type = y.get('type')
            if y_type == 'model':
                self.dkg.import_model(**(y['args']))

            if y_type == 'audio':
                self.dkg.log_inference(**(y['args']))
                sample_rate, data = y['value']
                file_path = processing_utils.save_audio_to_cache(
                    data, sample_rate, format=self.format, cache_dir=self.GRADIO_CACHE
                )
                print(file_path)
                orig_name = Path(file_path).name
                out['audio'] = dict(FileData(path=file_path, orig_name=orig_name))

        out['graph_data'] = self.dkg.to_json()
        print(out)
        return out
        

    def api_info(self) -> dict[str, Any]:
        return {"type": "string"}

    def example_inputs(self) -> Any:
        return "Hello!!"
