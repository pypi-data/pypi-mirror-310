from ._factory import mobilenet_v3_small, mobilenet_v3_large, mobilenet_configs

__all__ = [
    "MOBILENET_V3_ENTRYPOINT",
    "MOBILENET_V3_CONFIG",
]

MOBILENET_V3_ENTRYPOINT = {
    "mobilenet_v3_small": mobilenet_v3_small,
    "mobilenet_v3_large": mobilenet_v3_large,
}

MOBILENET_V3_CONFIG = {
    "mobilenet_v3_small": mobilenet_configs["mobilenet_v3_small"],
    "mobilenet_v3_large": mobilenet_configs["mobilenet_v3_large"],
}