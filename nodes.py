from typing import Tuple

import PIL
import numpy as np
import torch
from PIL import Image
from torch import Tensor

import folder_paths
from comfy import model_management
from comfy.taesd.taesd import TAESD

class TAESDVaeDecode:
    @classmethod
    def INPUT_TYPES(cls):  # type: ignore
        return {
            "required": {
                "latent": ("LATENT",),
                "vae": (folder_paths.get_filename_list("vae_approx"), {})
            }
        }

    RETURN_TYPES = ("IMAGE",)
    FUNCTION = "decode"
    OUTPUT_IS_LIST = (False,)
    CATEGORY = "conditioning"

    def __init__(self):
        self.taesd = None

    def decode(self, latent: torch.Tensor, vae: str) -> Tuple[torch.Tensor]:
        if self.taesd is None:
            self.taesd = TAESD(None, folder_paths.get_full_path("vae_approx", vae)).to(model_management.get_torch_device())

        x_sample = self.taesd.decoder((latent['samples'].to(model_management.get_torch_device()) * 0.18215))[0].detach()
        x_sample = x_sample.sub(0.5).mul(2)
        x_sample = torch.clamp((x_sample + 1.0) / 2.0, min=0.0, max=1.0)
        # x_sample = x_sample.movedim(1, -1)
        x_sample = x_sample.permute(1, 2, 0)

        # x_sample = 255. * np.moveaxis(x_sample.cpu().numpy(), 0, 2)
        # x_sample = x_sample.astype(np.uint8)

        return (torch.unsqueeze(x_sample, 0),)
