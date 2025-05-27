import logging
from etl.extract import DataExtractor
from etl.transform import DataTransformer
from analysis.mba import MarketBasketAnalyzer
from analysis.visualization import MBAResultsVisualizer
import pandas as pd
import os

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('mba_analysis.log'),
        logging.StreamHandler()
    ]
)

def main():
    """Main execution pipeline for Market Basket Analysis"""
    logger.info("Starting Market Basket Analysis Pipeline")
    
    try:
        # Step 1: Extract data
        logger.info("Extracting transaction data from database")
        extractor = DataExtractor()
        transaction_data = extractor.extract_transaction_data()
        
        # Step 2: Transform data and generate rules
        logger.info("Generating association rules")
        transformer = DataTransformer(min_support=0.01, min_confidence=0.3)
        results = transformer.generate_association_rules(transaction_data)
        
        # Step 3: Analyze results
        analyzer = MarketBasketAnalyzer(min_lift=1.5, top_n=20)
        significant_rules = analyzer.filter_significant_rules(results['association_rules'])
        recommendations = analyzer.generate_recommendations(significant_rules)
        
        # Calculate potential impact
        transaction_count = transaction_data['transaction_id'].nunique()
        potential_impact = analyzer.calculate_potential_impact(
            significant_rules, 
            transaction_count
        )
        
        # Step 4: Visualize results
        visualizer = MBAResultsVisualizer()
        visualizer.plot_top_rules(significant_rules)
        visualizer.plot_network_graph(recommendations)
        
        # Save results
        os.makedirs('output', exist_ok=True)
        significant_rules.to_csv('output/significant_rules.csv', index=False)
        
        logger.info(f"Market Basket Analysis completed successfully. Potential impact: {potential_impact:.0f} additional items sold")
        
    except Exception as e:
        logger.error(f"Pipeline failed: {e}", exc_info=True)
        raise

if __name__ == "__main__":
    main()
