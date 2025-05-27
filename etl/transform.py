import pandas as pd
import logging
from typing import List, Dict
from mlxtend.preprocessing import TransactionEncoder
from mlxtend.frequent_patterns import apriori, association_rules

logger = logging.getLogger(__name__)

class DataTransformer:
    """Transforms raw transaction data into MBA-ready format"""
    
    def __init__(self, min_support: float = 0.01, min_confidence: float = 0.3):
        self.min_support = min_support
        self.min_confidence = min_confidence
        
    def _prepare_transaction_data(self, df: pd.DataFrame) -> List[List[str]]:
        """Group items by transaction"""
        transactions = df.groupby('transaction_id')['product_name'].apply(list).values.tolist()
        return transactions
    
    def _encode_transactions(self, transactions: List[List[str]]) -> pd.DataFrame:
        """One-hot encode transaction data"""
        te = TransactionEncoder()
        te_ary = te.fit(transactions).transform(transactions)
        return pd.DataFrame(te_ary, columns=te.columns_)
    
    def generate_association_rules(self, df: pd.DataFrame) -> Dict[str, pd.DataFrame]:
        """
        Generate frequent itemsets and association rules
        Returns:
            Dictionary containing 'frequent_itemsets' and 'association_rules'
        """
        try:
            # Prepare transaction data
            transactions = self._prepare_transaction_data(df)
            encoded_df = self._encode_transactions(transactions)
            
            # Generate frequent itemsets
            frequent_itemsets = apriori(
                encoded_df, 
                min_support=self.min_support, 
                use_colnames=True
            )
            frequent_itemsets['length'] = frequent_itemsets['itemsets'].apply(lambda x: len(x))
            
            # Generate association rules
            rules = association_rules(
                frequent_itemsets, 
                metric="confidence", 
                min_threshold=self.min_confidence
            )
            rules = rules.sort_values('lift', ascending=False)
            
            return {
                'frequent_itemsets': frequent_itemsets,
                'association_rules': rules
            }
            
        except Exception as e:
            logger.error(f"Failed to generate association rules: {e}")
            raise
