# PTM Productivity Nodes
# Copyright (c) 2026 ParaTorMal
# Licensed under the MIT License

# __init__.py
# ParaTorMal custom nodes init
# from .filnavn import classnavn
import inspect
from . import PTM_nodes      # <— dette er viktig
from .PTM_nodes import *     # importerer klassene inn i globals()

# print("#################")
# print("PTM INIT CLASSES:", [k for k, v in globals().items() if k.startswith("PTM_")])


# Finn alle PTM-klasser i modulen
all_classes = {
    name: cls
    for name, cls in PTM_nodes.__dict__.items()
    if inspect.isclass(cls) and name.startswith("PTM_")
}

# Class mappings
NODE_CLASS_MAPPINGS = all_classes

# Display names
NODE_DISPLAY_NAME_MAPPINGS = {
    name: getattr(cls, "DISPLAY_NAME", name)
    for name, cls in all_classes.items()
}

# Add a little notice to the loading screen just for fun!
VERSION = "1.0.0"

print("══════════════════════════════════════════════════════════════════════════════════")
print(f"Entering ParaTorMal Activity mode!  PTM ComfyUI Nodes v{VERSION}")
print(f"Loaded {len(NODE_CLASS_MAPPINGS)} PTM node(s)")
print("══════════════════════════════════════════════════════════════════════════════════")


# print("PTM FINAL CLASS MAP:", NODE_CLASS_MAPPINGS)
# print("PTM FINAL DISPLAY MAP:", NODE_DISPLAY_NAME_MAPPINGS)



