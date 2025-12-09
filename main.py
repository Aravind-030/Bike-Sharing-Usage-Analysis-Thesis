import os
from src.data_loader import BikeDataLoader
from src.analysis import BikeAnalyzer

def main():
    # Ensure output directory exists
    if not os.path.exists('output'):
        os.makedirs('output')

    # Step 1: Initialize Data Loader
    # Ensure your CSV files are in a 'data' folder
    loader = BikeDataLoader(
        hourly_path='data/hour.csv', 
        daily_path='data/day.csv'
    )
    
    # Step 2: Load and Clean Data
    clean_df = loader.load_and_clean()
    
    # Step 3: Initialize Analyzer
    analyzer = BikeAnalyzer(clean_df)
    
    # Step 4: Execute Analyses
    print("--- Starting Analysis ---")
    analyzer.plot_temporal_trends()
    analyzer.plot_user_segmentation()
    print("--- Analysis Complete. Check 'output' folder. ---")

if __name__ == "__main__":
    main()
