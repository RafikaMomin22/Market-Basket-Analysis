# Market-Basket-Analysis


# Market Basket Analysis Implementation

This project implements Market Basket Analysis (MBA) to identify frequently co-purchased products, enabling optimization of promotions and cross-sell strategies. 
PLEASE KEEP IN MIND THIS IS A SIMPLIFIED VERSION, as I cannot provide the complete code for privacy-binding reasons. 

## Features

- ETL pipeline for extracting transaction data from SQL databases
- Association rule mining using Apriori algorithm
- Rule filtering and recommendation generation
- Visualization of association rules and product networks
- Unit testing and logging

## Business Impact

The analysis helps:
- Identify product affinities for targeted promotions
- Optimize product placement and bundling
- Increase average basket size (demonstrated 12% increase in implementation)

## Installation

1. Clone the repository
2. Install requirements: `pip install -r requirements.txt`
3. Configure database settings in `config/settings.py`

## Usage

Run the main pipeline:
```bash
python main.py
