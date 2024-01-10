from time import time
import numpy as np
import soundfile as sf

from .util import *

# Basic inference
def log_inference(
    self,
    mode: str,
    model_name: str,
    sample_rate: int,
    seed: int,
    output: np.ndarray,
    **kwargs
) -> bool:
    mode = mode.lower()
    current_time = int(time())

    # TODO: handle single audio sample case
    if output.ndim == 2: output = np.expand_dims(output, axis=0)
    assert output.ndim == 3, "ndim must be 3"

    # Create batch node and edge from model
    sample_prefix = f'{model_name}_{seed}_{current_time}'
    batch_name = f'batch_{sample_prefix}'
    self.G.add_node(
        batch_name,
        alias=f'{model_name[:3]}_{batch_name[-10:]}',
        type='batch',
        created=current_time,
    )
    self.G.add_edge(
        model_name,
        batch_name,
        type=f'dd_{mode}',
        model_name=model_name,
        created=current_time,
        **kwargs
    )

    '''
    # Variation case
    if mode == 'variation':
        self.G.edges[model_name, batch_name]['noise_level'] = noise_level
        self.G.add_edge(
            audio_source_name,
            batch_name,
            type='audio_source',
            strength=round(1 - noise_level, 5)
        )
    '''

    # Create individual samples
    batch_dir = check_dir(self.root / audio_dir / mode / model_name)
    for i, sample in enumerate(output):
        # Save audio
        batch_index = i + 1
        audio_name = f'sample_{sample_prefix}_{batch_index}'
        audio_path = batch_dir / f'{audio_name}.wav'
        open(str(audio_path), 'a').close()
        sf.write(str(audio_path), sample, sample_rate)

        # Create node
        self.G.add_node(
            audio_name,
            alias=f'{model_name[:3]}_{batch_name[-10:]}_{batch_index}',
            batch_index=batch_index,
            type='audio',
            path=str(audio_path),
            sample_rate=sample_rate,
            created=current_time,
            parent=batch_name,
            **kwargs
        )
        '''
        self.G.add_edge(
            audio_name,
            batch_name,
            type='batch_split',
            created=current_time
        )
        '''
    return True
