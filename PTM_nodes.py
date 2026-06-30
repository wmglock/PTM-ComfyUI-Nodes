# PTM Productivity Nodes
# Copyright (c) 2026 ParaTorMal
# Licensed under the MIT License

# PTM Node Framework
# Alle PTM-noder autodiscoveres via __init__.py
# DISPLAY_NAME må være definert i hver klasse
# Klasse-navn må starte med PTM_ for at systemet skal plukke dem opp



import torch
import numpy as np
import comfy.sample
import comfy.sd
from PIL import Image
import random
import re
import folder_paths
import os

# Add a little notice to the loading screen just for fun!
VERSION = "1.0.0"

print("══════════════════════════════════════════════════════════════════════════════════")
print(f"Entering ParaTorMal Activity mode!  PTM ComfyUI Nodes v{VERSION}")
print(f"Loaded {len(NODE_CLASS_MAPPINGS)} PTM node(s)")
print("══════════════════════════════════════════════════════════════════════════════════")

# Nodes!
# 📌 ParaTorMal/QuickHacks
#  → PTM_SettingsHack
#  → PTM_QuickSettings
#  → PTM_ResolutionPicker
# 
#   
#   
#
# ══════════════════════════════════════════════════════════════════════════════════ First Node

class PTM_SettingsHack:
    DISPLAY_NAME = "📌PTM Settings Hack"
    
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "width": ("INT", {"default": 480, "min": 1, "max": 8192}),
                "height": ("INT", {"default": 720, "min": 1, "max": 8192}),
                "swap_wh": ("BOOLEAN", {"default": False}),
                "frames": ("INT", {"default": 81, "min": 1, "max": 5000}),
                "FramesPerSecond": ("INT", {"default": 24, "min": 1, "max": 240}),
                "Seconds": (["5","6","7","8","9","10"],),
                "int1": ("INT", {"default": 337}),
                "int2": ("INT", {"default": 337}),
                "int3": ("INT", {"default": 337}),
                "custom_text": ("STRING", {"default": "ParaTorMal"}),
            }
        }

    RETURN_TYPES = ("INT","INT","INT","INT","INT","INT","INT","INT","STRING")
    RETURN_NAMES = ("Width","Height","Frames","FPS","Length","INT1","INT2","INT3","Text")

    FUNCTION = "run"
    CATEGORY = "📌 ParaTorMal"

    def run(self, width, height, swap_wh, frames, FramesPerSecond, Seconds, int1, int2, int3, custom_text):

        Seconds = int(Seconds)
        Length = Seconds * FramesPerSecond

        if swap_wh:
            width, height = height, width

        return (width, height, frames, FramesPerSecond, Length, int1, int2, int3, custom_text)

# ══════════════════════════════════════════════════════════════════════════════════ New Node


class PTM_QuickSettings:
    DISPLAY_NAME = "📌PTM Quick Settings"
    
    SecPresets = ["5", "6", "7", "8", "9", "10"]

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "width": ("INT", {"default": 480, "min": 1, "max": 8192}),
                "height": ("INT", {"default": 720, "min": 1, "max": 8192}),
                "swap_wh": ("BOOLEAN", {"default": False}),
                "frames": ("INT", {"default": 81, "min": 1, "max": 5000}),
                "FramesPerSecond": ("INT", {"default": 24, "min": 1, "max": 240}),
                "Seconds": (["5","6","7","8","9","10"],),
            }
        }

    RETURN_TYPES = (
        "INT", "INT", "INT", "INT", "INT"
    )

    RETURN_NAMES = (
        "Width",
        "Height",
        "Frames",
        "FramesPerSecond",
        "Length"
    )

    FUNCTION = "run"
    CATEGORY = "📌 ParaTorMal"

    def run(self, width, height, swap_wh, frames, FramesPerSecond, Seconds):

        Seconds = int(Seconds)
        Length = Seconds * FramesPerSecond

        if swap_wh:
            width, height = height, width

        return (width, height, frames, FramesPerSecond, Length)

# ══════════════════════════════════════════════════════════════════════════════════ New Node



class PTM_ResolutionPicker:
    DISPLAY_NAME = "📌PTM Resolution Picker"

    @classmethod
    def INPUT_TYPES(cls):
        sizes = ["380","420","480","540","600","640","720","800","900","960","1080","1200","1280"]
        return {
            "required": {
                "width": (sizes, {"default": "480"}),
                "height": (sizes, {"default": "720"}),
                "swap_wh": ("BOOLEAN", {"default": False}),
            }
        }

    RETURN_TYPES = ("INT", "INT")
    RETURN_NAMES = ("Width", "Height")

    FUNCTION = "run"
    CATEGORY = "📌 ParaTorMal"

    def run(self, width, height, swap_wh):

        # Convert selections from strings to ints
        width = int(width)
        height = int(height)

        # Swap if toggle is enabled
        if swap_wh:
            width, height = height, width

        return (width, height)




# ══════════════════════════════════════════════════════════════════════════════════ New Node




class PTM_WildPrompts:
    DISPLAY_NAME = "📌PTM WildPrompts"

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "text": ("STRING", {
                    "multiline": True,
                    "default": "A north norwegian man wearing $[colors] coveralls holding a {coffee cup | fishing rod | wrench | shotgun}. He looks at the camera and says: {jau | næh | dæven steike | no begynne æ å bli småirritert}."
                }),
                "seed": ("INT", {
                    "default": 337,
                    "min": 0,
                    "max": 0xffffffffffffffff
                }),
                "repeat_last": ("BOOLEAN", {"default": False}),
            }
        }

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("Text",)
    FUNCTION = "run"
    CATEGORY = "📌 ParaTorMal"

    _last_result = None


    def run(self, text, seed, repeat_last):
        if repeat_last and self._last_result is not None:
            return (self._last_result,)

        rng = random.Random(seed)
        result = self.process_text(text, rng)

        self._last_result = result
        return (result,)

    def process_text(self, text, rng):
        # Inline: {red | blue | green}
        def replace_inline(match):
            content = match.group(1)
            options = [x.strip() for x in content.split("|") if x.strip()]
            if not options:
                return match.group(0)
            return rng.choice(options)

        # File wildcard: $[colors] -> models/ptm/colors.txt
        def replace_file(match):
            name = match.group(1).strip()

            safe_name = name.replace("\\", "/").strip("/")
            file_path = os.path.join(folder_paths.models_dir, "ptm", safe_name + ".txt")

            if not os.path.exists(file_path):
                return f"[MISSING: {safe_name}.txt]"

            try:
                with open(file_path, "r", encoding="utf-8") as f:
                    lines = [
                        line.strip()
                        for line in f.readlines()
                        if line.strip() and not line.strip().startswith("#")
                    ]

                if not lines:
                    return f"[EMPTY: {safe_name}.txt]"

                return rng.choice(lines)

            except Exception as e:
                return f"[ERROR: {safe_name}.txt - {e}]"

        result = text

        # Kjør flere runder for nested wildcards
        for _ in range(10):
            old = result
            result = re.sub(r"\{([^{}]+)\}", replace_inline, result)
            result = re.sub(r"\$\[([^\[\]]+)\]", replace_file, result)

            if result == old:
                break

        return result


        
# ══════════════════════════════════════════════════════════════════════════════════ END
# 
#
# keep everything below this point at the end if adding more nodes!

