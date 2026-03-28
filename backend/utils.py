"""
Utility functions for VeriGraph backend
- UUID generation
- Score normalization
- Text processing
- Device configuration
"""

import uuid
from typing import Tuple, List, Dict, Any
import numpy as np
import torch


def generate_request_id() -> str:
    """Generate a unique request ID"""
    return str(uuid.uuid4())[:8]


def normalize_score(value: float, min_val: float = 0.0, max_val: float = 100.0) -> float:
    """
    Normalize a score to a specific range
    
    Args:
        value: The value to normalize
        min_val: Minimum value for range
        max_val: Maximum value for range
    
    Returns:
        Normalized score
    """
    return np.clip(value, min_val, max_val)


def calculate_confidence(scores: List[float]) -> float:
    """
    Calculate confidence based on score consistency
    
    Args:
        scores: List of scores from different models
    
    Returns:
        Confidence score between 0 and 1
    """
    if not scores:
        return 0.5
    
    variance = np.var(scores)
    # Lower variance = higher confidence
    confidence = 1.0 / (1.0 + variance)
    return float(np.clip(confidence, 0.0, 1.0))


def truncate_text(text: str, max_tokens: int = 128) -> str:
    """
    Truncate text to maximum tokens (rough approximation)
    
    Args:
        text: Text to truncate
        max_tokens: Maximum number of tokens
    
    Returns:
        Truncated text
    """
    # Simple approximation: ~1 token = 4 characters
    max_chars = max_tokens * 4
    if len(text) > max_chars:
        return text[:max_chars] + "..."
    return text


def get_device() -> torch.device:
    """
    Get the appropriate computing device (GPU/CPU)
    
    Returns:
        torch.device object
    """
    if torch.cuda.is_available():
        return torch.device("cuda")
    elif torch.backends.mps.is_available():
        return torch.device("mps")  # Metal Performance Shaders for macOS
    else:
        return torch.device("cpu")


def batch_iterator(items: List[Any], batch_size: int = 32):
    """
    Create batches from a list for efficient processing
    
    Args:
        items: List of items to batch
        batch_size: Size of each batch
    
    Yields:
        Batches of items
    """
    for i in range(0, len(items), batch_size):
        yield items[i : i + batch_size]


def parse_verdict_options(options_str: str) -> Dict[str, bool]:
    """
    Parse verdict options from string (e.g., "contradicts:true, entails:false")
    
    Args:
        options_str: Options as string
    
    Returns:
        Dictionary of verdict options
    """
    options = {}
    try:
        for option in options_str.split(","):
            key, val = option.strip().split(":")
            options[key.strip()] = val.strip().lower() == "true"
    except (ValueError, IndexError):
        # If parsing fails, return empty
        pass
    return options


def format_score_display(score: int, max_score: int = 100) -> str:
    """
    Format score for display with emoji
    
    Args:
        score: The score value
        max_score: Maximum possible score
    
    Returns:
        Formatted score string
    """
    percentage = (score / max_score) * 100
    
    if percentage < 20:
        emoji = "✅"
    elif percentage < 40:
        emoji = "⚠️"
    elif percentage < 60:
        emoji = "❓"
    elif percentage < 80:
        emoji = "🚩"
    else:
        emoji = "❌"
    
    return f"{emoji} {score}/100"


def calculate_source_credibility_weight(
    sources: List[Dict[str, Any]], weights: List[float] = None
) -> float:
    """
    Calculate weighted average credibility of sources
    
    Args:
        sources: List of source dictionaries with credibility scores
        weights: Optional weights for each source
    
    Returns:
        Weighted average credibility
    """
    if not sources:
        return 0.5
    
    credibilities = [s.get("credibility", 0.5) for s in sources]
    
    if weights is None:
        weights = [1.0 / len(credibilities)] * len(credibilities)
    
    # Normalize weights
    weights = [w / sum(weights) for w in weights]
    
    weighted_avg = sum(c * w for c, w in zip(credibilities, weights))
    return float(np.clip(weighted_avg, 0.0, 1.0))
