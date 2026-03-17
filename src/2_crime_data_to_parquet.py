import pandas as pd

df = pd.read_csv(
    "data/processed/processed_vancouver_crime_data_2025.csv"
)

df.to_parquet(
    "data/processed/van_crime_data_2025.parquet",
    index=False
)
