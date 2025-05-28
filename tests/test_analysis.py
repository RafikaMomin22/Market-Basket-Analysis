import pytest
import pandas as pd
import numpy as np
from analysis.mba import MarketBasketAnalyzer
from pandas.testing import assert_frame_equal

@pytest.fixture
def sample_rules():
    return pd.DataFrame({
        'antecedents': [frozenset({'A'}), frozenset({'B'}), frozenset({'C'})],
        'consequents': [frozenset({'B'}), frozenset({'C'}), frozenset({'D'})],
        'support': [0.1, 0.05, 0.02],
        'confidence': [0.8, 0.6, 0.4],
        'lift': [2.5, 1.8, 1.2]
    })

def test_filter_significant_rules(sample_rules):
    analyzer = MarketBasketAnalyzer(min_lift=1.5, top_n=2)
    filtered = analyzer.filter_significant_rules(sample_rules)
    
    assert len(filtered) == 2
    assert filtered['lift'].min() >= 1.5
    assert filtered['confidence'].iloc[0] >= filtered['confidence'].iloc[1]

def test_generate_recommendations(sample_rules):
    analyzer = MarketBasketAnalyzer()
    recommendations = analyzer.generate_recommendations(sample_rules)
    
    assert 'A' in recommendations
    assert 'B' in recommendations
    assert 'C' in recommendations
    assert 'B' in recommendations['A']
    assert 'C' in recommendations['B']
    assert 'D' in recommendations['C']

def test_calculate_potential_impact(sample_rules):
    analyzer = MarketBasketAnalyzer()
    impact = analyzer.calculate_potential_impact(sample_rules, 1000)
    
    assert isinstance(impact, float)
    assert impact > 0
