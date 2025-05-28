import os
from typing import Dict, Any

class Settings:
    """Configuration settings for the MBA project"""
    
    # Database configuration
    DB_DRIVER: str = os.getenv("DB_DRIVER", "ODBC Driver 17 for SQL Server")
    DB_SERVER: str = os.getenv("DB_SERVER", "localhost")
    DB_NAME: str = os.getenv("DB_NAME", "retail_db")
    DB_USER: str = os.getenv("DB_USER", "mba_user")
    DB_PASSWORD: str = os.getenv("DB_PASSWORD", "secure_password")
    
    # Analysis parameters
    MIN_SUPPORT: float = float(os.getenv("MIN_SUPPORT", "0.01"))
    MIN_CONFIDENCE: float = float(os.getenv("MIN_CONFIDENCE", "0.3"))
    MIN_LIFT: float = float(os.getenv("MIN_LIFT", "1.5"))
    
    # Path configuration
    DATA_RAW_PATH: str = os.path.join("data", "raw")
    DATA_PROCESSED_PATH: str = os.path.join("data", "processed")
    
    @classmethod
    def to_dict(cls) -> Dict[str, Any]:
        """Return settings as dictionary"""
        return {
            k: v for k, v in cls.__dict__.items() 
            if not k.startswith("__") and not callable(v)
        }

# Singleton instance
settings = Settings()
