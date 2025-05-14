import pandas as pd
import pyodbc
from sqlalchemy import create_engine
from config import settings
import logging
from typing import Tuple

logger = logging.getLogger(__name__)

class DataExtractor:
    """Handles data extraction from SQL database"""
    
    def __init__(self):
        self.connection_string = (
            f"DRIVER={settings.DB_DRIVER};"
            f"SERVER={settings.DB_SERVER};"
            f"DATABASE={settings.DB_NAME};"
            f"UID={settings.DB_USER};"
            f"PWD={settings.DB_PASSWORD}"
        )
        
    def _test_connection(self) -> bool:
        """Test database connection"""
        try:
            conn = pyodbc.connect(self.connection_string)
            conn.close()
            return True
        except Exception as e:
            logger.error(f"Connection test failed: {e}")
            return False
    
    def extract_transaction_data(self) -> pd.DataFrame:
        """
        Extract transaction data from SQL database
        Returns:
            DataFrame with columns: transaction_id, product_id, product_name, category
        """
        if not self._test_connection():
            raise ConnectionError("Database connection failed")
            
        query = """
        SELECT 
            t.transaction_id,
            p.product_id,
            p.product_name,
            p.category
        FROM transactions t
        JOIN transaction_items ti ON t.transaction_id = ti.transaction_id
        JOIN products p ON ti.product_id = p.product_id
        WHERE t.transaction_date BETWEEN DATEADD(month, -3, GETDATE()) AND GETDATE()
        """
        
        try:
            engine = create_engine(f"mssql+pyodbc:///?odbc_connect={self.connection_string}")
            df = pd.read_sql(query, engine)
            logger.info(f"Successfully extracted {len(df)} records")
            return df
        except Exception as e:
            logger.error(f"Data extraction failed: {e}")
            raise
