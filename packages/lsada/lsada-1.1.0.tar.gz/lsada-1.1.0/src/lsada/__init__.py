"""
LSADA - Language Services and Data Analysis
A flexible evaluation framework for content using LLMs
"""

__version__ = "1.0.0"

from .evaluator import Evaluator
from .models import LLMManager, BaseLLMClient
from .config import ConfigManager, config_manager
from .utils import MetricsCalculator, LLMResponseParser

__all__ = [
    'Evaluator',
    'LLMManager',
    'BaseLLMClient',
    'ConfigManager',
    'config_manager',
    'MetricsCalculator',
    'LLMResponseParser'
]
