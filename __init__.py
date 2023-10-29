from custom_nodes.Comfy_OtherVAEs.nodes import TAESDVaeDecode

NODE_CLASS_MAPPINGS = {
    "OtherVAE_Taesd": TAESDVaeDecode,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "OtherVAE_Taesd": "TAESD VAE Decode",
}
