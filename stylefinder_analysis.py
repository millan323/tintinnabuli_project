import pandas as pd

# Load the CSV file with your extracted features
df = pd.read_csv("stylefinder_features.csv")

# Show the first few rows
print("🎼 StyleFinder Dataset Preview:")
print(df.head())

# Show some basic statistics
print("\n📊 Summary Statistics:")
print(df.describe(include="all"))
