from importlib.metadata import version, PackageNotFoundError

from nanofed.cli import client_main, server_main
from nanofed.communication import HTTPClient, HTTPServer
from nanofed.orchestration import Coordinator, CoordinatorConfig
from nanofed.server import FedAvgAggregator, ModelManager
from nanofed.trainer import TorchTrainer

__all__ = [
    "client_main",
    "server_main",
    "HTTPClient",
    "HTTPServer",
    "TorchTrainer",
    "Coordinator",
    "CoordinatorConfig",
    "FedAvgAggregator",
    "ModelManager",
]


try:
    __version__ = version("nanofed")
except PackageNotFoundError:
    __version__ = "unknown"
