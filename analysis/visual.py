import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import networkx as nx
from typing import Dict
import logging

logger = logging.getLogger(__name__)

class MBAResultsVisualizer:
    """Visualizes Market Basket Analysis results"""
    
    def __init__(self):
        sns.set_style("whitegrid")
        plt.rcParams['figure.figsize'] = (12, 8)
        
    def plot_top_rules(self, rules: pd.DataFrame, title: str = "Top Association Rules"):
        """Plot top association rules by confidence and lift"""
        plt.figure(figsize=(12, 8))
        
        # Prepare data
        rules['antecedents_str'] = rules['antecedents'].apply(lambda x: ', '.join(list(x)))
        rules['consequents_str'] = rules['consequents'].apply(lambda x: ', '.join(list(x)))
        rules['rule'] = rules.apply(lambda x: f"{x['antecedents_str']} → {x['consequents_str']}", axis=1)
        
        # Create subplots
        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 12))
        
        # Confidence plot
        sns.barplot(x='confidence', y='rule', data=rules, ax=ax1, palette='Blues_d')
        ax1.set_title('Confidence Level of Association Rules')
        ax1.set_xlabel('Confidence')
        ax1.set_ylabel('')
        
        # Lift plot
        sns.barplot(x='lift', y='rule', data=rules, ax=ax2, palette='Greens_d')
        ax2.set_title('Lift Value of Association Rules')
        ax2.set_xlabel('Lift')
        ax2.set_ylabel('')
        
        plt.tight_layout()
        plt.savefig('association_rules.png', bbox_inches='tight', dpi=300)
        plt.close()
        
    def plot_network_graph(self, recommendations: Dict[str, List[str]], top_n: int = 15):
        """Create network graph of product associations"""
        G = nx.Graph()
        
        # Add nodes and edges
        for product, recs in list(recommendations.items())[:top_n]:
            G.add_node(product)
            for rec in recs[:5]:  # Top 5 recommendations per product
                G.add_node(rec)
                G.add_edge(product, rec)
                
        # Draw graph
        plt.figure(figsize=(15, 15))
        pos = nx.spring_layout(G, k=0.5)
        
        nx.draw_networkx_nodes(G, pos, node_size=2000, alpha=0.8, node_color='skyblue')
        nx.draw_networkx_edges(G, pos, width=1.5, alpha=0.5, edge_color='gray')
        nx.draw_networkx_labels(G, pos, font_size=10, font_family='sans-serif')
        
        plt.title('Product Recommendation Network', fontsize=15)
        plt.axis('off')
        plt.savefig('product_recommendation_network.png', bbox_inches='tight', dpi=300)
        plt.close()
