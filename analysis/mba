import pandas as pd
import logging
from typing import Dict, List
import numpy as np

logger = logging.getLogger(__name__)

class MarketBasketAnalyzer:
    """Analyzes and interprets market basket analysis results"""
    
    def __init__(self, min_lift: float = 1.5, top_n: int = 20):
        self.min_lift = min_lift
        self.top_n = top_n
        
    def filter_significant_rules(self, rules: pd.DataFrame) -> pd.DataFrame:
        """Filter rules by lift and sort by confidence"""
        significant_rules = rules[
            (rules['lift'] >= self.min_lift) & 
            (rules['confidence'] >= rules['confidence'].quantile(0.75))
        ].sort_values('confidence', ascending=False)
        
        return significant_rules.head(self.top_n)
    
    def generate_recommendations(self, rules: pd.DataFrame) -> Dict[str, List[str]]:
        """Generate product recommendations from association rules"""
        recommendations = {}
        
        for _, row in rules.iterrows():
            antecedents = list(row['antecedents'])
            consequents = list(row['consequents'])
            
            for ant in antecedents:
                if ant not in recommendations:
                    recommendations[ant] = []
                recommendations[ant].extend([c for c in consequents if c not in recommendations[ant]])
                
        return recommendations
    
    def calculate_potential_impact(self, rules: pd.DataFrame, transaction_count: int) -> float:
        """Estimate potential revenue impact from implementing recommendations"""
        if len(rules) == 0:
            return 0.0
            
        avg_basket_size_increase = rules['confidence'].mean() * 0.5  # Conservative estimate
        potential_impact = transaction_count * avg_basket_size_increase
        
        logger.info(f"Estimated potential basket size increase: {avg_basket_size_increase:.2f} items per transaction")
        logger.info(f"Potential total impact: {potential_impact:.0f} additional items sold")
        
        return potential_impact
