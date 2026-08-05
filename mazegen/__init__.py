from .config_parser import read_config, ConfigError
from .generator import MazeGenerator
#from .solver import dfs_alg
__all__ = [
    "read_config",
    "ConfigError",
    "MazeGenerator"
    ]
