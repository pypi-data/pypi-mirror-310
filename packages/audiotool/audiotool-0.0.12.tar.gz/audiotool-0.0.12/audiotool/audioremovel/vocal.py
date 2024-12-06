import os
from pathlib import Path
from urllib.parse import urlparse
from loguru import logger
import torch
from .uvr5.mdxnet import Predictor
import soundfile as sf


def get_filename_from_url(url):
    return os.path.basename(urlparse(url).path)


class AudioSeparatorOne:

    def __init__(self, model_type="mel_band_roformer") -> None:
        self.model_type = model_type
        if "mel_band_roformer" in self.model_type:
            from .uvr5.mel_band_roformer_infer import AudioSeparator

            self.model = AudioSeparator()
            logger.info(f"audio separator using {self.model_type} model")
        elif "mdxnet" in self.model_type:
            # source https://github.com/TRvlvr/model_repo/releases/tag/all_public_uvr_models
            available_models = {
                "mdxnet-main": "https://github.com/TRvlvr/model_repo/releases/download/all_public_uvr_models/UVR-MDX-NET-Inst_Main.onnx",
                "mdxnet-voc-ft": "",
            }
            if self.model_type not in available_models:
                raise Exception(f"Model {self.model_type} not found")
            model_path = f"checkpoints/{get_filename_from_url(available_models[self.model_type])}"
            if not os.path.exists(model_path):
                logger.info(
                    f"downloading {self.model_type} model from {available_models[self.model_type]}"
                )
                torch.hub.download_url_to_file(
                    available_models[self.model_type], model_path, progress=True
                )
                logger.info(f"{self.model_type} model downloaded successfully.")
            self.model_path = model_path
            mdx_config = {
                "output": Path("temp/"),
                "model_path": self.model_path,
                "denoise": True,
                "margin": 44100,
                "chunks": 15,
                "n_fft": 6144,
                "dim_t": 8,
                "dim_f": 2048,
            }
            # todo: add default model path
            self.model = Predictor(**mdx_config)
        else:
            raise Exception("Model not found")

    def separate(self, audio_file, output_dir=None):
        if "mdxnet" in self.model_type:
            vocals, no_vocals, sampling_rate = self.model.predict(audio_file)
            base_name = os.path.splitext(os.path.basename(audio_file))[0]

            if output_dir is None:
                vocal_path = os.path.join(output_dir, f"{base_name}_vocals.wav")
                inst_path = os.path.join(output_dir, f"{base_name}_instrumental.wav")
            else:
                vocal_path = os.path.join(output_dir, f"{base_name}_vocals.wav")
                inst_path = os.path.join(output_dir, f"{base_name}_instrumental.wav")

            sf.write(
                vocal_path,
                vocals,
                sampling_rate,
            )
            sf.write(
                inst_path,
                no_vocals,
                sampling_rate,
            )
            return {"vocals": vocal_path, "instrumental": inst_path}

        else:
            return self.model.separate(audio_file, output_dir=output_dir)
