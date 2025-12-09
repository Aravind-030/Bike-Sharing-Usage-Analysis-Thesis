import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

class BikeAnalyzer:
    def __init__(self, dataframe):
        self.df = dataframe
        self.conn = sqlite3.connect(':memory:')
        self._setup_db()

    def _setup_db(self):
        """Internal method to load dataframe into SQLite."""
        self.df.to_sql('rentals', self.conn, index=False, if_exists='replace')

    def plot_temporal_trends(self, output_path='output/temporal_analysis.png'):
        """Generates SQL-based temporal analysis chart."""
        query = """
        SELECT hour, day_type, AVG(total_rentals) as avg_rentals 
        FROM rentals 
        GROUP BY hour, day_type 
        ORDER BY day_type, hour
        """
        data = pd.read_sql_query(query, self.conn)
        
        plt.figure(figsize=(12, 6))
        sns.lineplot(data=data, x='hour', y='avg_rentals', hue='day_type', marker="o")
        plt.title('Hourly Bike Demand: Commuter vs Leisure Patterns')
        plt.grid(True, linestyle='--', alpha=0.7)
        plt.savefig(output_path)
        plt.close()
        print(f"Saved temporal analysis to {output_path}")

    def plot_user_segmentation(self, output_path='output/user_analysis.png'):
        """Analyzes Registered vs Casual behavior by weather."""
        # 1=Clear, 4=Heavy Rain
        weather_avg = self.df.groupby('weather_code')[['casual', 'registered']].mean()
        
        weather_avg.plot(kind='bar', stacked=True, figsize=(10, 6))
        plt.title('User Resilience to Weather Conditions')
        plt.ylabel('Average Rentals')
        plt.savefig(output_path)
        plt.close()
        print(f"Saved user analysis to {output_path}")
