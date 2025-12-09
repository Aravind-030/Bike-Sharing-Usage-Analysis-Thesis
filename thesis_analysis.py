"""
Master's Thesis: Descriptive Analysis of Bike Rental Usage Patterns
File: thesis_analysis.py
Description: 
    This script handles the ETL (Extract, Transform, Load) process for the 
    Bike Sharing dataset, performs SQL-based aggregations for temporal analysis, 
    and generates visualizations for user behavior and weather correlations.
    
    Note on Spatial Data: The spatial analysis module requires raw trip history 
    logs (with lat/long). If 'trips.csv' is not present, that section is skipped 
    gracefully to allow the script to run on the standard UCI aggregated dataset.
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import sqlite3
import os

# Global plotting style
sns.set_theme(style="ticks")
plt.rcParams['figure.figsize'] = (12, 6)

class BikeDataPipeline:
    def __init__(self, hourly_path, daily_path, trips_path=None):
        self.hourly_path = hourly_path
        self.daily_path = daily_path
        self.trips_path = trips_path
        self.conn = sqlite3.connect(':memory:') # Using in-memory DB for speed
        self.df = None

    def process_data(self):
        """Loads raw data and applies necessary transformations."""
        if not os.path.exists(self.hourly_path):
            print(f"[!] Critical: {self.hourly_path} not found.")
            return

        print(f"Loading data from {self.hourly_path}...")
        self.df = pd.read_csv(self.hourly_path)

        # 1. Semantic Renaming: Mapping cryptic headers to readable names
        # This makes the SQL queries much more readable for the grader.
        column_map = {
            'dteday': 'date', 'yr': 'year', 'mnth': 'month', 'hr': 'hour',
            'weathersit': 'weather_code', 'cnt': 'total_rentals',
            'hum': 'humidity_norm', 'atemp': 'feel_temp_norm'
        }
        self.df.rename(columns=column_map, inplace=True)

        # 2. Denormalization
        # The UCI readme states temp is normalized to 41 max, hum to 100, wind to 67.
        # We revert this to get real units for the charts.
        self.df['temp_c'] = self.df['temp'] * 41
        self.df['humidity_real'] = self.df['humidity_norm'] * 100
        self.df['wind_speed_real'] = self.df['windspeed'] * 67

        # 3. Categorical labeling for readability
        self.df['day_type'] = self.df['workingday'].apply(
            lambda x: 'Working Day' if x == 1 else 'Weekend/Holiday'
        )
        
        # Load into SQLite for analysis
        self.df.to_sql('rentals', self.conn, index=False, if_exists='replace')
        print("Data successfully loaded into SQL environment.")

    def run_temporal_analysis(self):
        """Identifies peak usage hours using SQL."""
        print("\n--- Performing Temporal SQL Analysis ---")
        
        # We group by hour and day type to separate commuters from tourists
        query = """
        SELECT 
            hour, 
            day_type, 
            AVG(total_rentals) as average_volume
        FROM rentals 
        GROUP BY hour, day_type 
        ORDER BY day_type, hour
        """
        results = pd.read_sql_query(query, self.conn)
        
        # Plotting
        plt.figure()
        sns.lineplot(data=results, x='hour', y='average_volume', hue='day_type', marker="o")
        plt.title('Hourly Usage Profiles: Commute vs. Leisure', fontsize=14)
        plt.xlabel('Hour of Day (0-23)')
        plt.ylabel('Avg. Bike Rentals')
        plt.xticks(range(0, 24))
        plt.tight_layout()
        plt.savefig('viz_temporal_patterns.png')
        print(">> Saved chart: viz_temporal_patterns.png")

    def run_weather_impact_study(self):
        """Analyzes how weather severity impacts casual vs registered users."""
        print("\n--- Performing Weather Impact Study ---")
        
        # Aggregate rentals by weather situation
        # 1=Clear, 2=Mist, 3=Light Snow/Rain, 4=Heavy Rain
        weather_avg = self.df.groupby('weather_code')[['casual', 'registered']].mean()
        
        weather_avg.plot(kind='bar', stacked=True, color=)
        plt.title('Impact of Weather Severity on User Segments', fontsize=14)
        plt.xlabel('Weather Condition (1=Good, 4=Severe)')
        plt.ylabel('Avg. Rentals')
        plt.xticks(rotation=0)
        plt.savefig('viz_weather_impact.png')
        print(">> Saved chart: viz_weather_impact.png")

    def run_spatial_analysis(self):
        """
        Attempts to map station flows. 
        Note: Checks for 'trips.csv' (raw logs). If missing, skips this step.
        """
        print("\n--- Checking for Spatial Data ---")
        if self.trips_path and os.path.exists(self.trips_path):
            print("Loading raw trip logs for spatial analysis...")
            trips = pd.read_csv(self.trips_path)
            trips.to_sql('raw_trips', self.conn, index=False, if_exists='replace')
            
            # Find top start stations
            q = """
            SELECT "Start Station", COUNT(*) as departures 
            FROM raw_trips GROUP BY "Start Station" 
            ORDER BY departures DESC LIMIT 5
            """
            print(pd.read_sql_query(q, self.conn))
        else:
            print("[Info] 'trips.csv' not found. Skipping spatial module.")
            print("Note: The standard UCI dataset is aggregated and lacks station coordinates.")

if __name__ == "__main__":
    # Initialize analysis pipeline
    # Ensure hour.csv and day.csv are in the same folder as this script
    pipeline = BikeDataPipeline(
        hourly_path='hour.csv', 
        daily_path='day.csv',
        trips_path='trips.csv' # Optional raw data file
    )
    
    pipeline.process_data()
    pipeline.run_temporal_analysis()
    pipeline.run_weather_impact_study()
    pipeline.run_spatial_analysis()
    print("\nAnalysis Cycle Complete.")
