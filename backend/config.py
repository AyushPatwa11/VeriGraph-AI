"""
Configuration settings for VeriGraph backend
"""

import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


class Config:
    """Base configuration"""
    
    # Flask
    DEBUG = False
    TESTING = False
    
    # API
    JSON_SORT_KEYS = False
    JSONIFY_PRETTYPRINT_REGULAR = True
    
    # Logging
    LOG_LEVEL = "INFO"
    
    # CORS
    CORS_ORIGINS = ["*"]
    
    # Cache
    CACHE_TYPE = "simple"  # simple, redis
    CACHE_DEFAULT_TIMEOUT = 300
    CACHE_MAX_SIZE = 1000
    
    # Models
    VERIFICATION_MODEL = os.getenv("VERIFICATION_MODEL", "cross-encoder/qnli-deberta-large")
    CLAIM_DECOMPOSITION_MODEL = os.getenv("CLAIM_DECOMPOSITION_MODEL", "t5-base")
    RETRIEVAL_MODEL = os.getenv("RETRIEVAL_MODEL", "sentence-transformers/all-mpnet-base-v2")
    
    # Device
    DEVICE = os.getenv("DEVICE", "auto")  # "cpu", "cuda", "auto"
    
    # Verification
    VERIFICATION_TIMEOUT = int(os.getenv("VERIFICATION_TIMEOUT", "30"))
    CACHE_ENABLED = os.getenv("CACHE_ENABLED", "true").lower() == "true"
    
    # Data paths
    DATA_DIR = os.path.join(os.path.dirname(__file__), "..", "data")
    MODELS_DIR = os.path.join(DATA_DIR, "models")
    CACHE_DIR = os.path.join(DATA_DIR, "cache")


class DevelopmentConfig(Config):
    """Development configuration"""
    DEBUG = True
    TESTING = False
    LOG_LEVEL = "DEBUG"


class TestingConfig(Config):
    """Testing configuration"""
    TESTING = True
    CACHE_DEFAULT_TIMEOUT = 0
    CACHE_MAX_SIZE = 100


class ProductionConfig(Config):
    """Production configuration"""
    DEBUG = False
    CACHE_TYPE = "redis"
    CACHE_MAX_SIZE = 10000


# Configuration dictionary
config = {
    "development": DevelopmentConfig,
    "testing": TestingConfig,
    "production": ProductionConfig,
    "default": DevelopmentConfig,
}


def get_config(env=None):
    """Get configuration for environment"""
    if env is None:
        env = os.getenv("FLASK_ENV", "development")
    
    config_class = config.get(env, config["default"])
    return config_class()
