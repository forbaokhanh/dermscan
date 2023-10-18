import pandas as pd

# Define the path to the CSV file
file_path = "./data/stuff.csv"

# Read the CSV file into a Pandas DataFrame
try:
    df = pd.read_csv(file_path, sep=",")
except FileNotFoundError:
    print(f"File not found at {file_path}")
    exit(1)
except Exception as e:
    print(f"An error occurred: {e}")
    exit(1)

# Display the first few rows of the DataFrame
print(df.head())
print(df.info())

