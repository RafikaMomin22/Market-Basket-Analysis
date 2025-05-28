import pandas as pd
import logging
from typing import Dict
from pathlib import Path
from config import settings

logger = logging.getLogger(__name__)

class DataLoader:
    """Handles saving of processed data and results"""
    
    def __init__(self):
        Path(settings.DATA_PROCESSED_PATH).mkdir(parents=True, exist_ok=True)
        
    def save_processed_data(self, data: Dict[str, pd.DataFrame]) -> None:
        """
        Save processed data to disk
        Args:
            data: Dictionary of DataFrames to save
        """
        try:
            for name, df in data.items():
                path = Path(settings.DATA_PROCESSED_PATH) / f"{name}.parquet"
                df.to_parquet(path)
                logger.info(f"Saved {name} to {path}")
        except Exception as e:
            logger.error(f"Failed to save processed data: {e}")
            raise
            
    def save_recommendations(self, recommendations: Dict[str, list], filename: str) -> None:
        """
        Save product recommendations to CSV
        Args:
            recommendations: Dictionary of product recommendations
            filename: Output filename
        """
        try:
            rec_df = pd.DataFrame(
                [(k, ", ".join(v)) for k, v in recommendations.items()],
                columns=["product", "recommendations"]
            )
            path = Path(settings.DATA_PROCESSED_PATH) / filename
            rec_df.to_csv(path, index=False)
            logger.info(f"Saved recommendations to {path}")
        except Exception as e:
            logger.error(f"Failed to save recommendations: {e}")
            raise
