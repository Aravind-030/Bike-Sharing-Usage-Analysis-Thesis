import pandas as pd
import os

class BikeDataLoader:
    """
    Handles the Extraction, Transformation, and Loading (ETL) of bike data.
    """
    def __init__(self, hourly_path, daily_path):
        self.hourly_path = hourly_path
        self.daily_path = daily_path
        self.df = None

    def load_and_clean(self):
        """Loads CSVs and applies semantic renaming."""
        if not os.path.exists(self.hourly_path):
            raise FileNotFoundError(f"Data file not found at: {self.hourly_path}")

        print(f"Loading data from {self.hourly_path}...")
        self.df = pd.read_csv(self.hourly_path)

        # Semantic Renaming for readability
        rename_map = {
            'dteday': 'date', 'yr': 'year', 'mnth': 'month', 'hr': 'hour',
            'weathersit': 'weather_code', 'cnt': 'total_rentals',
            'hum': 'humidity_norm', 'atemp': 'feel_temp_norm',
            'workingday': 'is_working_day'
        }
        self.df.rename(columns=rename_map, inplace=True)

        # Type Conversion
        self.df['date'] = pd.to_datetime(self.df['date'])

        # Feature Engineering: De-normalize weather data for human readability
        # (Constants derived from UCI dataset documentation)
        self.df['temp_c'] = self.df['temp'] * 41
        self.df['humidity_real'] = self.df['humidity_norm'] * 100
        self.df['wind_speed_real'] = self.df['windspeed'] * 67
        
        # Create readable labels
        self.df['day_type'] = self.df['is_working_day'].apply(
            lambda x: 'Working Day' if x == 1 else 'Weekend/Holiday'
        )
        
        return self.df
